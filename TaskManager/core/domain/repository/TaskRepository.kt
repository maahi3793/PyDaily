package com.taskmanager.core.domain.repository

import com.taskmanager.core.domain.model.Task
import kotlinx.coroutines.flow.Flow
import java.util.UUID

/**
 * Repository interface in the Domain layer.
 * Defines the contract for data operations without exposing data source details.
 */
interface TaskRepository {
    
    suspend fun insertTask(task: Task)
    
    suspend fun updateTask(task: Task)
    
    suspend fun deleteTask(task: Task)
    
    suspend fun getTaskById(taskId: UUID): Task?
    
    fun getAllTasks(): Flow<List<Task>>
    
    fun getTasksDueToday(startOfDay: Long, endOfDay: Long): Flow<List<Task>>
    
    fun getSubtasksByParentId(parentTaskId: UUID): Flow<List<Task>>
    
    fun getAllSubtasksGroupedByParent(): Flow<List<Task>>
    
    fun getIncompleteRecurrentTasks(): Flow<List<Task>>
}
