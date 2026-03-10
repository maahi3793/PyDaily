package com.taskmanager.core.domain.usecase

import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.TaskRepository
import com.taskmanager.core.domain.scheduler.TaskAlarmScheduler
import java.util.UUID

/**
 * Handles completing a task, specifically bridging the gap from Notification Action Buttons
 * to Recurrence logic and Alarm Rescheduling.
 * 
 * Expands upon `CompleteTaskUseCase` from Phase 1 by integrating the `TaskAlarmScheduler`.
 */
class HandleTaskCompletionUseCase(
    private val repository: TaskRepository,
    private val alarmScheduler: TaskAlarmScheduler
) {

    suspend operator fun invoke(taskId: UUID) {
        val task = repository.getTaskById(taskId)
            ?: throw IllegalArgumentException("Task with id $taskId not found.")

        if (task.isCompleted) return

        // Cancel the current alarm just in case someone marks it complete before it fires
        alarmScheduler.cancel(task)

        if (task.recurrenceIntervalMinutes != null) {
            handleRecurringTaskCompletion(task)
        } else {
            val completedTask = task.copy(isCompleted = true)
            repository.updateTask(completedTask)
        }
    }

    private suspend fun handleRecurringTaskCompletion(currentTask: Task) {
        val intervalMs = currentTask.recurrenceIntervalMinutes!! * 60 * 1000L
        val now = System.currentTimeMillis()

        val nextDueDate = (currentTask.dueDate ?: now) + intervalMs
        
        if (currentTask.recurrenceEndDate != null && nextDueDate > currentTask.recurrenceEndDate) {
            val completedTask = currentTask.copy(isCompleted = true)
            repository.updateTask(completedTask)
            return
        }

        // 1. Mark current as complete
        val completedCurrentTask = currentTask.copy(isCompleted = true)
        repository.updateTask(completedCurrentTask)

        // 2. Generate next iteration
        val nextStartDate = currentTask.startDate?.let { it + intervalMs }
        val nextTask = currentTask.copy(
            id = UUID.randomUUID(), 
            isCompleted = false,
            createdAt = now,
            startDate = nextStartDate,
            dueDate = nextDueDate
        )
        
        // 3. Save the new future task iteration to DB
        repository.insertTask(nextTask)

        // 4. Critically: Schedule the NEW exact alarm for the future iteration
        alarmScheduler.schedule(nextTask)
    }
}
