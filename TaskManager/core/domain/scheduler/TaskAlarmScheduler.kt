package com.taskmanager.core.domain.scheduler

import com.taskmanager.core.domain.model.Task

/**
 * Interface for scheduling exact task alarms.
 * Abstracted to remain entirely within the Domain layer.
 */
interface TaskAlarmScheduler {
    
    /**
     * Schedules an exact alarm. Depending on the Task data
     * (e.g. dueDate or a recurrence timestamp), this will fire precisely.
     */
    fun schedule(task: Task)
    
    /**
     * Cancels an existing alarm for the specified task.
     */
    fun cancel(task: Task)
}
