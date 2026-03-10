package com.taskmanager.core.domain.usecase

import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.TaskRepository
import java.util.UUID

/**
 * Use Case to mark a task as completed.
 * CRITICAL LOGIC: Handles recurring tasks by automatically generating
 * the next instance of the task if recurrenceIntervalMinutes is set.
 */
class CompleteTaskUseCase(
    private val repository: TaskRepository
) {

    suspend operator fun invoke(taskId: UUID) {
        val task = repository.getTaskById(taskId)
            ?: throw IllegalArgumentException("Task with id $taskId not found.")

        if (task.isCompleted) {
            return // Task is already completed, nothing to do
        }

        if (task.recurrenceIntervalMinutes != null) {
            // Task has a recurrence interval.
            // Automatically generate the next instance of the task instead of just completing this one.
            handleRecurringTaskCompletion(task)
        } else {
            // Standard non-recurring task completion
            val completedTask = task.copy(isCompleted = true)
            repository.updateTask(completedTask)
        }
    }

    private suspend fun handleRecurringTaskCompletion(currentTask: Task) {
        val intervalMs = currentTask.recurrenceIntervalMinutes!! * 60 * 1000L
        val now = System.currentTimeMillis()

        // 1. Check if we have surpassed the recurrenceEndDate.
        // If an end date is specified and the next occurrence would be past it,
        // we just mark the current one completed and do NOT generate a new one.
        val nextDueDate = (currentTask.dueDate ?: now) + intervalMs
        
        if (currentTask.recurrenceEndDate != null && nextDueDate > currentTask.recurrenceEndDate) {
            val completedTask = currentTask.copy(isCompleted = true)
            repository.updateTask(completedTask)
            return
        }

        // 2. We need to generate the next instance.
        // In this implementation, we mark the *current* task as complete,
        // and create a *new* Task entity for the future occurrence to preserve history.
        // Alternatively, you could just update the due date of the existing task if history isn't needed,
        // but creating a new instance is generally better for analytics and historical tracking.
        
        val completedCurrentTask = currentTask.copy(isCompleted = true)
        repository.updateTask(completedCurrentTask)

        // Generate next task based on the completed task
        val nextStartDate = currentTask.startDate?.let { it + intervalMs }
        
        val nextTask = currentTask.copy(
            id = UUID.randomUUID(), // Must be a new UUID
            isCompleted = false,
            createdAt = now,
            startDate = nextStartDate,
            dueDate = nextDueDate
        )
        
        repository.insertTask(nextTask)
    }
}
