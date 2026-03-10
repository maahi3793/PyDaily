package com.taskmanager.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.taskmanager.core.domain.model.Task
import com.taskmanager.ui.components.TaskCard
import com.taskmanager.ui.theme.BrandYellow
import com.taskmanager.ui.viewmodel.TaskViewModel

/**
 * A tablet/landscape optimized split-screen that plots repeating tasks on a visual timeline.
 */
@Composable
fun CalendarSplitScreen(
    viewModel: TaskViewModel
) {
    val todaysTasks by viewModel.todaysTasks.collectAsStateWithLifecycle()

    Row(modifier = Modifier.fillMaxSize()) {
        // Left Segment: Standard Task List
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
        ) {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp)
            ) {
                item {
                    Text(
                        text = "Task List",
                        style = MaterialTheme.typography.headlineSmall,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                }
                items(
                    items = todaysTasks,
                    key = { it.id }
                ) { task ->
                    TaskCard(
                        task = task,
                        onComplete = { viewModel.completeTask(task.id) },
                        onDelete = { viewModel.deleteTask(task) },
                        onClick = { /* Navigate or highlight */ }
                    )
                }
            }
        }

        // Divider
        VerticalDivider(modifier = Modifier.fillMaxHeight())

        // Right Segment: Graphical Timeline (Canvas)
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .padding(16.dp)
        ) {
            DailyTimelineVisualizer(
                tasks = todaysTasks,
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

/**
 * Custom Canvas drawing a single vertical line representing the day,
 * and plotting tasks as dots along it.
 */
@Composable
private fun DailyTimelineVisualizer(
    tasks: List<Task>,
    modifier: Modifier = Modifier
) {
    val lineColor = MaterialTheme.colorScheme.outlineVariant

    Canvas(modifier = modifier) {
        val width = size.width
        val height = size.height

        val xCenter = width / 2f
        
        // Draw the main vertical timeline axis
        drawLine(
            color = lineColor,
            start = Offset(xCenter, 0f),
            end = Offset(xCenter, height),
            strokeWidth = 4.dp.toPx()
        )

        // Plot tasks
        val startOfDay = System.currentTimeMillis() - (System.currentTimeMillis() % 86400000)
        val endOfDay = startOfDay + 86400000

        tasks.forEach { task ->
            if (task.dueDate != null) {
                // Determine vertical position mapping task time to Canvas height
                val timeRatio = (task.dueDate.toFloat() - startOfDay.toFloat()) / (endOfDay - startOfDay).toFloat()
                
                // Only plot if it falls within "today"
                if (timeRatio in 0f..1f) {
                    val yPosition = height * timeRatio

                    // Color indicator: Yellow for recurring (interval exists), Primary otherwise
                    val nodeColor = if (task.recurrenceIntervalMinutes != null) BrandYellow else Color.Gray

                    drawCircle(
                        color = nodeColor,
                        radius = 12.dp.toPx(),
                        center = Offset(xCenter, yPosition)
                    )
                }
            }
        }
    }
}
