package com.taskmanager.core.domain.model

import java.util.UUID

/**
 * Domain model representing a Task.
 * This is the core business object decoupled from the Room database entity.
 */
data class Task(
    val id: UUID,
    val title: String,
    val description: String?,
    val isCompleted: Boolean,
    val createdAt: Long,
    val startDate: Long?,
    val dueDate: Long?,
    val recurrenceIntervalMinutes: Int?,
    val recurrenceEndDate: Long?,
    val parentTaskId: UUID?,
    val estimatedTimeMinutes: Int?
)
