package com.taskmanager.core.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

/**
 * Represents a Task in the local Room database.
 * This is the core entity mapping to the "tasks" table.
 * It's structured for an offline-first architecture.
 */
@Entity(tableName = "tasks")
data class TaskEntity(
    @PrimaryKey val id: UUID = UUID.randomUUID(),
    
    val title: String,
    
    val description: String? = null,
    
    val isCompleted: Boolean = false,
    
    // Stored as Unix timestamps (Long) - Room TypeConverters can be used later or primitive types are used directly
    val createdAt: Long = System.currentTimeMillis(),
    
    val startDate: Long? = null,
    
    val dueDate: Long? = null,
    
    // Support intra-day micro-repeating logic, e.g., "every 120 minutes"
    val recurrenceIntervalMinutes: Int? = null,
    
    val recurrenceEndDate: Long? = null,
    
    // For infinite nesting of subtasks
    val parentTaskId: UUID? = null,
    
    // For AI time blocking
    val estimatedTimeMinutes: Int? = null
)
