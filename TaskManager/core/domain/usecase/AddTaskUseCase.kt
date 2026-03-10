package com.taskmanager.core.domain.usecase

import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.TaskRepository
import java.util.UUID

/**
 * Use Case to add a new task.
 * Encapsulates the business logic and validation for creating a task.
 */
class AddTaskUseCase(
    private val repository: TaskRepository
) {

    /**
     * @throws IllegalArgumentException if title is blank.
     */
    suspend operator fun invoke(task: Task) {
        if (task.title.isBlank()) {
            throw IllegalArgumentException("Task title cannot be empty.")
        }
        
        // Additional business logic validations could go here
        // e.g., validating that dueDate is after startDate
        
        repository.insertTask(task)
    }
}
