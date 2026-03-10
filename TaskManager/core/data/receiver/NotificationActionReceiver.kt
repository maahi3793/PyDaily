package com.taskmanager.core.data.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.taskmanager.core.data.notification.TaskNotificationManager
import com.taskmanager.core.domain.usecase.HandleTaskCompletionUseCase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.UUID

/**
 * Handles actions dispatched directly from the Notification UI.
 * This runs entirely in the background, interacting natively with the Domain layer logic.
 */
class NotificationActionReceiver : BroadcastReceiver() {

    // Normally injected
    // @Inject lateinit var handleTaskCompletionUseCase: HandleTaskCompletionUseCase
    // @Inject lateinit var notificationManager: TaskNotificationManager

    // For demonstration
    private var mockHandleTaskCompletionUseCase: HandleTaskCompletionUseCase? = null
    private var mockNotificationManager: TaskNotificationManager? = null

    override fun onReceive(context: Context, intent: Intent) {
        val taskIdString = intent.getStringExtra(TaskNotificationManager.EXTRA_TASK_ID) ?: return
        val taskId = UUID.fromString(taskIdString)

        val pendingResult = goAsync()

        CoroutineScope(Dispatchers.IO).launch {
            try {
                when (intent.action) {
                    TaskNotificationManager.ACTION_MARK_COMPLETE -> {
                        // Crucial Phase 2 Use Case: Completes the task AND schedules the next alarm iteratively.
                        mockHandleTaskCompletionUseCase?.invoke(taskId)
                        // mockHandleTaskCompletionUseCase(taskId)
                        
                        // Dismiss the notification natively once complete is handled
                        mockNotificationManager?.dismissNotification(taskId.hashCode())
                    }
                    TaskNotificationManager.ACTION_SNOOZE -> {
                        // Handle snoozing logic (e.g., creating a temporary +15 minute alarm)
                        // Leaving this implementation abstract but structurally ready
                        mockNotificationManager?.dismissNotification(taskId.hashCode())
                    }
                }
            } finally {
                pendingResult.finish()
            }
        }
    }
}
