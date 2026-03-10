package com.taskmanager.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.taskmanager.ui.theme.BrandBlue
import kotlinx.coroutines.delay

/**
 * A futuristic circular timer that uses `animateFloatAsState` for a fluid sweeping motion 
 * rather than rigid 1-second ticks.
 */
@Composable
fun FocusTimer(
    totalDurationSeconds: Int,
    remainingSeconds: Int,
    modifier: Modifier = Modifier
) {
    // Calculate the target progress value (0f to 1f)
    val targetProgress = if (totalDurationSeconds > 0) {
        remainingSeconds.toFloat() / totalDurationSeconds.toFloat()
    } else {
        0f
    }

    // The magic of fluid movement:
    // Instead of jumping instantly to the next integer slice, we tween the float 
    // over 1000ms linearly so the circle continuously sweeps down seamlessly.
    val animatedProgress by animateFloatAsState(
        targetValue = targetProgress,
        animationSpec = tween(
            durationMillis = 1000, 
            easing = LinearEasing
        ),
        label = "FluidTimerSweep"
    )

    Box(
        modifier = modifier.size(240.dp),
        contentAlignment = Alignment.Center
    ) {
        // Draw the background track and the animated sweep
        val trackColor = MaterialTheme.colorScheme.surfaceVariant
        val sweepColor = BrandBlue

        Canvas(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            val strokeWidth = 12.dp.toPx()
            
            // Background Track
            drawArc(
                color = trackColor,
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
            )

            // Animated Sweep
            drawArc(
                color = sweepColor,
                startAngle = -90f, // Start from the top
                sweepAngle = 360f * animatedProgress,
                useCenter = false,
                style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
            )
        }

        // Timer text formatting
        val minutes = remainingSeconds / 60
        val seconds = remainingSeconds % 60
        
        Text(
            text = String.format("%02d:%02d", minutes, seconds),
            style = MaterialTheme.typography.displayLarge.copy(
                fontWeight = FontWeight.Light,
                color = MaterialTheme.colorScheme.onBackground
            )
        )
    }
}
