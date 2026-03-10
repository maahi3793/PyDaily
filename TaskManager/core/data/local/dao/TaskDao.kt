package com.taskmanager.core.data.local.dao

import androidx.room.*
import com.taskmanager.core.data.local.entity.TaskEntity
import kotlinx.coroutines.flow.Flow
import java.util.UUID

@Dao
interface TaskDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTask(task: TaskEntity)

    @Update
    suspend fun updateTask(task: TaskEntity)

    @Delete
    suspend fun deleteTask(task: TaskEntity)

    @Query("SELECT * FROM tasks WHERE id = :taskId")
    suspend fun getTaskById(taskId: UUID): TaskEntity?

    @Query("SELECT * FROM tasks ORDER BY createdAt DESC")
    fun getAllTasks(): Flow<List<TaskEntity>>

    /**
     * Fetch tasks due today.
     * Takes the start and end of the day in Unix timestamp format to allow for timezone flexibility from the domain layer.
     */
    @Query("SELECT * FROM tasks WHERE dueDate >= :startOfDay AND dueDate <= :endOfDay ORDER BY dueDate ASC")
    fun getTasksDueToday(startOfDay: Long, endOfDay: Long): Flow<List<TaskEntity>>

    /**
     * Fetch tasks that are subtasks of a specific parent task.
     */
    @Query("SELECT * FROM tasks WHERE parentTaskId = :parentTaskId ORDER BY createdAt ASC")
    fun getSubtasksByParentId(parentTaskId: UUID): Flow<List<TaskEntity>>

    /**
     * Fetch tasks grouped by parentTaskId. 
     * In SQLite/Room, returning a flat list sorted by parentTaskId groups them logically for the UI or Domain layer to map.
     */
    @Query("SELECT * FROM tasks WHERE parentTaskId IS NOT NULL ORDER BY parentTaskId ASC, createdAt ASC")
    fun getAllSubtasksGroupedByParent(): Flow<List<TaskEntity>>

    /**
     * Fetch incomplete tasks that have a recurrenceIntervalMinutes set.
     */
    @Query("SELECT * FROM tasks WHERE isCompleted = 0 AND recurrenceIntervalMinutes IS NOT NULL ORDER BY dueDate ASC")
    fun getIncompleteRecurrentTasks(): Flow<List<TaskEntity>>
    
}
