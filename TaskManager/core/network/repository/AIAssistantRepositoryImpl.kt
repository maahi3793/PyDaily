package com.taskmanager.core.network.repository

import com.google.gson.Gson
import com.taskmanager.core.domain.repository.AIAssistantRepository
import com.taskmanager.core.network.model.AIChoiceDto
import com.taskmanager.core.network.model.AILLMRequestDto
import com.taskmanager.core.network.model.AILLMResponseDto
import com.taskmanager.core.network.model.AIMessageDto
import com.taskmanager.core.network.model.AITaskResponseDto
import retrofit2.http.Body
import retrofit2.http.POST

/**
 * Retrofit API definition
 */
interface LLMApiService {
    @POST("v1/chat/completions") // Abstract Endpoint
    suspend fun sendPrompt(@Body request: AILLMRequestDto): AILLMResponseDto
}

/**
 * Concrete implementation mapping LLM network requests and enforcing Prompt Engineering.
 */
class AIAssistantRepositoryImpl(
    private val apiService: LLMApiService,
    private val gson: Gson
) : AIAssistantRepository {

    override suspend fun parseNaturalLanguageToTask(input: String): Result<AITaskResponseDto> {
        return runCatching {
            val systemInstruction = """
                You are a strict JSON mapping assistant for an advanced Task Manager app.
                Parse the user's natural language request and output ONLY raw, valid JSON. 
                DO NOT output markdown formatting (like ```json), just the raw object.
                
                The current system time in milliseconds is: ${System.currentTimeMillis()}
                
                Calculate all `startDateMillis`, `dueDateMillis`, and `recurrenceEndDateMillis` as absolute Unix Timestamps based on this current time.
                Calculate `recurrenceIntervalMinutes` strictly as an Integer (e.g. 2 hours = 120).
                
                Strict JSON Schema requirement:
                {
                  "title": "String", (Required)
                  "description": "String or null",
                  "startDateMillis": "Long (Timestamp) or null",
                  "dueDateMillis": "Long (Timestamp) or null",
                  "recurrenceIntervalMinutes": "Integer or null",
                  "recurrenceEndDateMillis": "Long (Timestamp) or null"
                }
            """.trimIndent()

            val request = AILLMRequestDto(
                messages = listOf(
                    AIMessageDto(role = "system", content = systemInstruction),
                    AIMessageDto(role = "user", content = input)
                )
            )

            // Make the network call
            val response = apiService.sendPrompt(request)
            
            // Extract the purely generated JSON string
            val jsonContent = response.choices?.firstOrNull()?.message?.content
                ?: throw IllegalStateException("Empty response from LLM")
                
            // Safe JSON mapping
            gson.fromJson(jsonContent.trim(), AITaskResponseDto::class.java)
        }
    }
}
