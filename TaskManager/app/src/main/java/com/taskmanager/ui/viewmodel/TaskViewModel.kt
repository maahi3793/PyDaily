package com.taskmanager.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.TaskRepository
import com.taskmanager.core.domain.usecase.HandleTaskCompletionUseCase
import com.taskmanager.core.domain.usecase.ProcessNaturalLanguageUseCase
import com.taskmanager.core.domain.usecase.ScheduleTaskUseCase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.util.UUID

/**
 * Connects the Phase 3 UI Layer to Phase 1/2 Use Cases entirely via StateFlows.
 */
// @HiltViewModel
class TaskViewModel(
    private val taskRepository: TaskRepository,
    private val scheduleTaskUseCase: ScheduleTaskUseCase,
    private val processNaturalLanguageUseCase: ProcessNaturalLanguageUseCase,
    private val handleTaskCompletionUseCase: HandleTaskCompletionUseCase
) : ViewModel() {

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _aiError = MutableStateFlow<String?>(null)
    val aiError: StateFlow<String?> = _aiError

    // UI state exposing today's tasks dynamically from the SQLite DB flow
    val todaysTasks: StateFlow<List<Task>> = taskRepository.getTasksDueToday(
        startOfDay = getStartOfDayMillis(),
        endOfDay = getEndOfDayMillis()
    ).stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = emptyList()
    )
    
    // Tracks currently active Focus task
    private val _activeTimerTaskId = MutableStateFlow<UUID?>(null)
    val activeTimerTaskId: StateFlow<UUID?> = _activeTimerTaskId

    fun setActiveTimer(taskId: UUID?) {
        _activeTimerTaskId.value = taskId
    }

    /**
     * Completes a task triggering Phase 2 Alarms/Recurrence logically.
     */
    fun completeTask(taskId: UUID) {
        viewModelScope.launch {
            if (_activeTimerTaskId.value == taskId) {
                _activeTimerTaskId.value = null
            }
            handleTaskCompletionUseCase(taskId)
        }
    }

    /**
     * Deletes a task bypassing standard completion.
     */
    fun deleteTask(task: Task) {
        viewModelScope.launch {
            taskRepository.deleteTask(task)
            // Note: Should also cancel the alarm, abstracted here for Phase 3 focus
        }
    }

    /**
     * Submits Phase 2 LLM parsing request.
     */
    fun submitAIPrompt(prompt: String) {
        if (prompt.isBlank()) return
        
        viewModelScope.launch {
            _isLoading.value = true
            _aiError.value = null
            
            val result = processNaturalLanguageUseCase(prompt)
            
            result.onFailure { error ->
                _aiError.value = error.message ?: "Failed to process AI request"
            }
            
            _isLoading.value = false
        }
    }

    // Helper utilities for the Flow query
    private fun getStartOfDayMillis(): Long {
        return System.currentTimeMillis() - (System.currentTimeMillis() % 86400000) // Rough generic day start
    }
    
    private fun getEndOfDayMillis(): Long {
        return getStartOfDayMillis() + 86399999
    }
}
