package com.taskmanager.core.domain.usecase

import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.AIAssistantRepository
import java.util.UUID

/**
 * Takes a natural language string from the UI, asks the LLM to map it to JSON,
 * converts that JSON into a Domain Task Entity, and schedules it.
 */
class ProcessNaturalLanguageUseCase(
    private val aiRepository: AIAssistantRepository,
    private val scheduleTaskUseCase: ScheduleTaskUseCase
) {

    suspend operator fun invoke(inputText: String): Result<Task> {
        if (inputText.isBlank()) return Result.failure(IllegalArgumentException("Input is empty"))

        // 1. Call AI layer 
        return aiRepository.parseNaturalLanguageToTask(inputText).mapCatching { dto ->
            // 2. Map Network DTO to Domain Model
            val newTask = Task(
                id = UUID.randomUUID(),
                title = dto.title,
                description = dto.description,
                isCompleted = false,
                createdAt = System.currentTimeMillis(),
                startDate = dto.startDateMillis,
                dueDate = dto.dueDateMillis,
                recurrenceIntervalMinutes = dto.recurrenceIntervalMinutes,
                recurrenceEndDate = dto.recurrenceEndDateMillis,
                parentTaskId = null,
                estimatedTimeMinutes = null
            )

            // 3. Delegate to Scheduling Use Case (DB + Alarm)
            scheduleTaskUseCase(newTask)
            
            // Return created task to UI if necessary
            newTask
        }
    }
}
