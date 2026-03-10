package com.taskmanager.core.data.local.dao

import androidx.room.*
import com.taskmanager.core.data.local.entity.TagEntity
import kotlinx.coroutines.flow.Flow
import java.util.UUID

@Dao
interface TagDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTag(tag: TagEntity)

    @Update
    suspend fun updateTag(tag: TagEntity)

    @Delete
    suspend fun deleteTag(tag: TagEntity)

    @Query("SELECT * FROM tags WHERE id = :tagId")
    suspend fun getTagById(tagId: UUID): TagEntity?

    @Query("SELECT * FROM tags ORDER BY name ASC")
    fun getAllTags(): Flow<List<TagEntity>>
}
