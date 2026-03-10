package com.taskmanager.core.data.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.taskmanager.core.data.notification.TaskNotificationManager
import com.taskmanager.core.data.scheduler.TaskAlarmSchedulerImpl
import com.taskmanager.core.domain.repository.TaskRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.UUID

/**
 * Fires at the exact time calculated by the Scheduler.
 * Its sole responsibility is grabbing the task details from DB 
 * and calling the Notification Manager.
 */
class AlarmReceiver : BroadcastReceiver() {

    // Usually injected via @AndroidEntryPoint in Hilt
    // @Inject lateinit var taskRepository: TaskRepository
    // @Inject lateinit var notificationManager: TaskNotificationManager
    
    // For standalone compilation simulating injection
    private var mockTaskRepository: TaskRepository? = null
    private var mockNotificationManager: TaskNotificationManager? = null

    override fun onReceive(context: Context, intent: Intent) {
        val taskIdString = intent.getStringExtra(TaskAlarmSchedulerImpl.EXTRA_TASK_ID) ?: return
        val taskId = UUID.fromString(taskIdString)

        // goAsync() is generally needed if doing lengthy work, 
        // but for a quick DB pluck and Notification issuance a fast Coroutine is often sufficient
        val pendingResult = goAsync()

        CoroutineScope(Dispatchers.IO).launch {
            try {
                // val task = taskRepository.getTaskById(taskId)
                val task = mockTaskRepository?.getTaskById(taskId) // Simulated
                
                if (task != null && !task.isCompleted) {
                    // notificationManager.showTaskNotification(task)
                    mockNotificationManager?.showTaskNotification(task) // Simulated
                }
            } finally {
                pendingResult.finish()
            }
        }
    }
}
