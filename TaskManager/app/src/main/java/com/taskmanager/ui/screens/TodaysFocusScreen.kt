package com.taskmanager.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.taskmanager.ui.components.FocusTimer
import com.taskmanager.ui.components.TaskCard
import com.taskmanager.ui.components.TaskDetailSheet
import com.taskmanager.ui.theme.BrandBlue
import com.taskmanager.ui.viewmodel.TaskViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TodaysFocusScreen(
    viewModel: TaskViewModel,
    onNavigateToCalendar: () -> Unit
) {
    val todaysTasks by viewModel.todaysTasks.collectAsStateWithLifecycle()
    val activeTaskId by viewModel.activeTimerTaskId.collectAsStateWithLifecycle()
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle()

    var showBottomSheet by remember { mutableStateOf(false) }

    // Simulating a timer state for the UI, usually driven by a TickFlow in ViewModel
    val focusDurationSecs = 1500 // 25 minutes default Pomodoro
    var remainingSecs by remember { mutableStateOf(focusDurationSecs) }

    // Active Timer logic is simplified here to focus on the UI mapping capability
    LaunchedEffect(activeTaskId) {
        if (activeTaskId != null) {
            remainingSecs = focusDurationSecs
            // In a real app we'd collect a timer flow here
        }
    }

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(
                onClick = { showBottomSheet = true },
                containerColor = BrandBlue,
                contentColor = MaterialTheme.colorScheme.onPrimary
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add Task")
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 1. Prominent Focus Timer Area
            Spacer(modifier = Modifier.height(32.dp))
            
            Text(
                text = "Today's Focus",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            FocusTimer(
                totalDurationSeconds = focusDurationSecs,
                remainingSeconds = remainingSecs,
                modifier = Modifier.padding(bottom = 32.dp)
            )

            // Spinner during AI Request
            AnimatedVisibility(visible = isLoading, enter = fadeIn(), exit = fadeOut()) {
                LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
            }

            // 2. Constrained Task List (Max 5 items for "Focus")
            val focusedList = todaysTasks.take(5)
            
            LazyColumn(
                modifier = Modifier.fillMaxWidth().weight(1f)
            ) {
                items(
                    items = focusedList,
                    key = { it.id } // Required for proper compose list animations
                ) { task ->
                    TaskCard(
                        task = task,
                        onComplete = { viewModel.completeTask(task.id) },
                        onDelete = { viewModel.deleteTask(task) },
                        onClick = { 
                            // Either navigate to detail OR set as active timer
                            viewModel.setActiveTimer(task.id)
                        }
                    )
                }
                
                item { 
                    Spacer(modifier = Modifier.height(80.dp)) // FAB padding
                }
            }
        }
    }

    if (showBottomSheet) {
        TaskDetailSheet(
            onDismissRequest = { showBottomSheet = false },
            onSubmitPrompt = { prompt -> viewModel.submitAIPrompt(prompt) }
        )
    }
}
