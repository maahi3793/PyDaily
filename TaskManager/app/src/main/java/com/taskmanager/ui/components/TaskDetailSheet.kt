package com.taskmanager.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.taskmanager.ui.theme.BrandBlue
import com.taskmanager.ui.theme.GlassAlphaLight

/**
 * A ModalBottomSheet acting as both task creator and AI Prompt ingestor.
 * Features early concepts for Glassmorphism by modifying container alphas.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TaskDetailSheet(
    onDismissRequest: () -> Unit,
    onSubmitPrompt: (String) -> Unit,
    sheetState: SheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
) {
    var promptText by remember { mutableStateOf("") }
    
    // Simulating Glassmorphism background for the sheet
    val glassmorphicColor = MaterialTheme.colorScheme.surface.copy(alpha = GlassAlphaLight)

    ModalBottomSheet(
        onDismissRequest = onDismissRequest,
        sheetState = sheetState,
        containerColor = glassmorphicColor,
        // The blur effect is technically only supported cleanly in Android 12+ (RenderEffect)
        // Without extensive custom drawing, setting the translucent surface color is the standard compose alternative
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp)
                .navigationBarsPadding(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "What's on your mind?",
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.onSurface
            )
            
            Spacer(modifier = Modifier.height(16.dp))

            // AI Natural Language Input Area
            OutlinedTextField(
                value = promptText,
                onValueChange = { promptText = it },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { 
                    Text("e.g. Remind me to drink water every 2 hours tomorrow") 
                },
                shape = RoundedCornerShape(16.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedBorderColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.5f),
                    focusedBorderColor = BrandBlue
                ),
                leadingIcon = {
                    // Futuristic multi-colored mic icon concept (using static tint for simplicity here)
                    Icon(Icons.Default.Mic, contentDescription = "Voice Input", tint = BrandBlue)
                },
                trailingIcon = {
                    if (promptText.isNotBlank()) {
                        IconButton(onClick = { 
                            onSubmitPrompt(promptText)
                            onDismissRequest() 
                        }) {
                            Icon(Icons.Default.Send, contentDescription = "Submit", tint = BrandBlue)
                        }
                    }
                }
            )
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
