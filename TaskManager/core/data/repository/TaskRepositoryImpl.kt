package com.taskmanager.core.data.repository

import com.taskmanager.core.data.local.dao.TaskDao
import com.taskmanager.core.data.local.entity.TaskEntity
import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.repository.TaskRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.util.UUID

// Dependency injection normally handles injecting TaskDao (e.g., via Hilt @Inject)
class TaskRepositoryImpl(
    private val taskDao: TaskDao
) : TaskRepository {

    override suspend fun insertTask(task: Task) {
        taskDao.insertTask(task.toEntity())
    }

    override suspend fun updateTask(task: Task) {
        taskDao.updateTask(task.toEntity())
    }

    override suspend fun deleteTask(task: Task) {
        taskDao.deleteTask(task.toEntity())
    }

    override suspend fun getTaskById(taskId: UUID): Task? {
        return taskDao.getTaskById(taskId)?.toDomain()
    }

    override fun getAllTasks(): Flow<List<Task>> {
        return taskDao.getAllTasks().map { entities -> 
            entities.map { it.toDomain() } 
        }
    }

    override fun getTasksDueToday(startOfDay: Long, endOfDay: Long): Flow<List<Task>> {
        return taskDao.getTasksDueToday(startOfDay, endOfDay).map { entities -> 
            entities.map { it.toDomain() } 
        }
    }

    override fun getSubtasksByParentId(parentTaskId: UUID): Flow<List<Task>> {
        return taskDao.getSubtasksByParentId(parentTaskId).map { entities -> 
            entities.map { it.toDomain() } 
        }
    }

    override fun getAllSubtasksGroupedByParent(): Flow<List<Task>> {
        return taskDao.getAllSubtasksGroupedByParent().map { entities -> 
            entities.map { it.toDomain() } 
        }
    }

    override fun getIncompleteRecurrentTasks(): Flow<List<Task>> {
        return taskDao.getIncompleteRecurrentTasks().map { entities -> 
            entities.map { it.toDomain() } 
        }
    }
}

// Mappers directly as extension functions for simplicity, or could be in a separate Mapper class
private fun TaskEntity.toDomain(): Task {
    return Task(
        id = id,
        title = title,
        description = description,
        isCompleted = isCompleted,
        createdAt = createdAt,
        startDate = startDate,
        dueDate = dueDate,
        recurrenceIntervalMinutes = recurrenceIntervalMinutes,
        recurrenceEndDate = recurrenceEndDate,
        parentTaskId = parentTaskId,
        estimatedTimeMinutes = estimatedTimeMinutes
    )
}

private fun Task.toEntity(): TaskEntity {
    return TaskEntity(
        id = id,
        title = title,
        description = description,
        isCompleted = isCompleted,
        createdAt = createdAt,
        startDate = startDate,
        dueDate = dueDate,
        recurrenceIntervalMinutes = recurrenceIntervalMinutes,
        recurrenceEndDate = recurrenceEndDate,
        parentTaskId = parentTaskId,
        estimatedTimeMinutes = estimatedTimeMinutes
    )
}
