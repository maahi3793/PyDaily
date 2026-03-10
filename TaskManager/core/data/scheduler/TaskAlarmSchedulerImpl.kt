package com.taskmanager.core.data.scheduler

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import com.taskmanager.core.data.receiver.AlarmReceiver
import com.taskmanager.core.domain.model.Task
import com.taskmanager.core.domain.scheduler.TaskAlarmScheduler

/**
 * Concrete implementation mapping Domain requests to Android's native AlarmManager.
 */
class TaskAlarmSchedulerImpl(
    private val context: Context
) : TaskAlarmScheduler {

    private val alarmManager = context.getSystemService(AlarmManager::class.java)

    override fun schedule(task: Task) {
        // Find the absolute time this alarm should trigger (e.g., dueDate or next occurrence)
        // Defaulting to dueDate for the initial schedule. 
        val timeInMillis = task.dueDate ?: return 

        val intent = Intent(context, AlarmReceiver::class.java).apply {
            putExtra(TaskAlarmSchedulerImpl.EXTRA_TASK_ID, task.id.toString())
        }

        val pendingIntent = PendingIntent.getBroadcast(
            context,
            task.id.hashCode(), // Unique ID to ensure distinct pending intents per task
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // API 31+ requires declaring SCHEDULE_EXACT_ALARM permission
        // Use exact alarms strictly for precise, user-facing scheduling to respect Doze optimizations.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && !alarmManager.canScheduleExactAlarms()) {
            // Ideally notify user if permission is denied, 
            // for now fallback to inexact to guarantee firing eventually
            alarmManager.setAndAllowWhileIdle(
                AlarmManager.RTC_WAKEUP,
                timeInMillis,
                pendingIntent
            )
        } else {
            // Precise trigger handling Doze mode natively 
            alarmManager.setExactAndAllowWhileIdle(
                AlarmManager.RTC_WAKEUP,
                timeInMillis,
                pendingIntent
            )
        }
    }

    override fun cancel(task: Task) {
        val intent = Intent(context, AlarmReceiver::class.java)
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            task.id.hashCode(),
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        alarmManager.cancel(pendingIntent)
    }

    companion object {
        const val EXTRA_TASK_ID = "EXTRA_TASK_ID"
    }
}
