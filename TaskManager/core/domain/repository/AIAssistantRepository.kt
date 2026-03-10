package com.taskmanager.core.domain.repository

import com.taskmanager.core.network.model.AITaskResponseDto

/**
 * Interface abstracting the LLM communication from the Domain Use Cases.
 */
interface AIAssistantRepository {
    
    /**
     * Sends a natural language string and expects a perfectly parsed mapping.
     * @param input "Remind me to drink water every 2 hours starting tomorrow"
     * @return Formatted DTO mapped via strict JSON 
     */
    suspend fun parseNaturalLanguageToTask(input: String): Result<AITaskResponseDto>
}
