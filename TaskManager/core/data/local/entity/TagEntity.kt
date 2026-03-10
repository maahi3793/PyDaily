package com.taskmanager.core.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

/**
 * Represents a Tag in the database.
 * Tags are used to categorize tasks. They have a many-to-many relationship with Tasks.
 */
@Entity(tableName = "tags")
data class TagEntity(
    @PrimaryKey val id: UUID = UUID.randomUUID(),
    val name: String,
    val color: String // Hex color string, e.g., "#FF0000"
)
