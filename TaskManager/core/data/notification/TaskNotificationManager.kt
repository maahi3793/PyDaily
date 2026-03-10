package com.taskmanager.core.data.notification

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.taskmanager.core.data.receiver.NotificationActionReceiver
import com.taskmanager.core.domain.model.Task

/**
 * Manages the creation and display of system notifications.
 */
class TaskNotificationManager(
    private val context: Context
) {

    private val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

    init {
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val highPriorityChannel = NotificationChannel(
                CHANNEL_HIGH_PRIORITY,
                "High Priority Nudges",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Urgent tasks that require immediate attention."
                enableVibration(true)
            }

            val summaryChannel = NotificationChannel(
                CHANNEL_DAILY_SUMMARY,
                "Daily Summaries",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Daily breakdown of tasks."
            }

            notificationManager.createNotificationChannels(listOf(highPriorityChannel, summaryChannel))
        }
    }

    /**
     * Builds and displays the notification with action buttons.
     */
    fun showTaskNotification(task: Task) {
        val completeIntent = Intent(context, NotificationActionReceiver::class.java).apply {
            action = ACTION_MARK_COMPLETE
            putExtra(EXTRA_TASK_ID, task.id.toString())
        }
        val completePendingIntent = PendingIntent.getBroadcast(
            context,
            // Combine action ID and task ID to keep PendingIntents unique
            (ACTION_MARK_COMPLETE + task.id).hashCode(),
            completeIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val snoozeIntent = Intent(context, NotificationActionReceiver::class.java).apply {
            action = ACTION_SNOOZE
            putExtra(EXTRA_TASK_ID, task.id.toString())
        }
        val snoozePendingIntent = PendingIntent.getBroadcast(
            context,
            (ACTION_SNOOZE + task.id).hashCode(),
            snoozeIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, CHANNEL_HIGH_PRIORITY)
            .setSmallIcon(android.R.drawable.ic_popup_reminder) // Placeholder icon
            .setContentTitle("Task Reminder")
            .setContentText(task.title)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            // Action to complete the task directly from the notification
            .addAction(
                android.R.drawable.ic_menu_save, 
                "Mark Complete", 
                completePendingIntent
            )
            // Action to snooze the task
            .addAction(
                android.R.drawable.ic_popup_sync, 
                "Snooze", 
                snoozePendingIntent
            )
            .build()

        // Use the Task's hashCode as the notification ID so updates overwrite the specific task banner
        notificationManager.notify(task.id.hashCode(), notification)
    }

    fun dismissNotification(notificationId: Int) {
        notificationManager.cancel(notificationId)
    }

    companion object {
        const val CHANNEL_HIGH_PRIORITY = "high_priority_channel"
        const val CHANNEL_DAILY_SUMMARY = "daily_summary_channel"

        const val ACTION_MARK_COMPLETE = "com.taskmanager.ACTION_MARK_COMPLETE"
        const val ACTION_SNOOZE = "com.taskmanager.ACTION_SNOOZE"
        const val EXTRA_TASK_ID = "EXTRA_TASK_ID"
    }
}
