package com.taskmanager.core.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.taskmanager.core.data.local.dao.TagDao
import com.taskmanager.core.data.local.dao.TaskDao
import com.taskmanager.core.data.local.entity.TagEntity
import com.taskmanager.core.data.local.entity.TaskEntity
import com.taskmanager.core.data.local.entity.TaskTagCrossRef

@Database(
    entities = [
        TaskEntity::class,
        TagEntity::class,
        TaskTagCrossRef::class
    ],
    version = 1,
    exportSchema = false
)
// NOTE: TypeConverters for UUID would be needed here in a full app, 
// usually provided via a @TypeConverters annotation.
// e.g., @TypeConverters(UUIDConverter::class)
abstract class TaskDatabase : RoomDatabase() {

    abstract fun taskDao(): TaskDao
    
    abstract fun tagDao(): TagDao
    
    // Companion object for Room.databaseBuilder would typically go here 
    // or be provided exclusively via Hilt DI in the :app module.
}
