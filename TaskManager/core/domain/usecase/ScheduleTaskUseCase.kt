package com.taskmanager.core.domain.usecase

import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.TaskRepository
import com.taskmanager.core.domain.scheduler.TaskAlarmScheduler

/**
 * Replaces or wraps `AddTaskUseCase` from Phase 1.
 * Ensures that whenever a task is saved, its background alarm is also registered.
 */
class ScheduleTaskUseCase(
    private val repository: TaskRepository,
    private val alarmScheduler: TaskAlarmScheduler
) {

    suspend operator fun invoke(task: Task) {
        if (task.title.isBlank()) {
            throw IllegalArgumentException("Task title cannot be empty.")
        }

        // 1. Save to database (Core Architecture phase 1)
        repository.insertTask(task)

        // 2. Schedule the exact AlarmManager trigger (Phase 2)
        // Only schedule if there's a valid targeted time
        if (task.dueDate != null || task.recurrenceIntervalMinutes != null) {
            alarmScheduler.schedule(task)
        }
    }
}
