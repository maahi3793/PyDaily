package com.taskmanager.core.network.model

import com.google.gson.annotations.SerializedName

/**
 * Expected JSON output strictly enforced via the Prompt Template.
 * Maps cleanly to the Phase 1 TaskEntity.
 */
data class AITaskResponseDto(
    @SerializedName("title")
    val title: String,
    
    @SerializedName("description")
    val description: String?,
    
    @SerializedName("startDateMillis")
    val startDateMillis: Long?,
    
    @SerializedName("dueDateMillis")
    val dueDateMillis: Long?,
    
    @SerializedName("recurrenceIntervalMinutes")
    val recurrenceIntervalMinutes: Int?,
    
    @SerializedName("recurrenceEndDateMillis")
    val recurrenceEndDateMillis: Long?
)

/**
 * Standard request body for generic LLM endpoints (e.g. OpenAI/Gemini REST).
 */
data class AILLMRequestDto(
    @SerializedName("model")
    val model: String = "gemini-1.5-pro", // Examplar model
    @SerializedName("messages")
    val messages: List<AIMessageDto>
)

data class AIMessageDto(
    @SerializedName("role") val role: String,
    @SerializedName("content") val content: String
)

data class AILLMResponseDto(
    @SerializedName("choices")
    val choices: List<AIChoiceDto>?
)

data class AIChoiceDto(
    @SerializedName("message")
    val message: AIMessageDto
)
