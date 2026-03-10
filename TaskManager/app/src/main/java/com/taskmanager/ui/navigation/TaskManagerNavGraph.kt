package com.taskmanager.ui.navigation

import androidx.compose.animation.ExperimentalSharedTransitionApi
import androidx.compose.animation.SharedTransitionLayout
import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.taskmanager.ui.screens.CalendarSplitScreen
import com.taskmanager.ui.screens.TodaysFocusScreen
import com.taskmanager.ui.viewmodel.TaskViewModel

sealed class Screen(val route: String) {
    object Focus : Screen("focus")
    object Calendar : Screen("calendar")
}

/**
 * Standard Navigation mapping for Jetpack Compose.
 * Prepares the architectural bounds for future `SharedTransitionLayout` mappings 
 * between the Focus list and hypothetical Detail screens.
 */
@OptIn(ExperimentalSharedTransitionApi::class)
@Composable
fun TaskManagerNavGraph(
    navController: NavHostController,
    viewModel: TaskViewModel
) {
    // SharedTransitionLayout surrounds the NavHost in Compose 1.7.0+ 
    // to enable Shared Element geometric morphing between screens.
    SharedTransitionLayout {
        NavHost(
            navController = navController,
            startDestination = Screen.Focus.route
        ) {
            composable(Screen.Focus.route) {
                // Injecting the SharedTransitionScope into the screen allows specific UI elements 
                // e.g., a TaskCard `Modifier.sharedElement(...)` to morph smoothly when navigating.
                TodaysFocusScreen(
                    viewModel = viewModel,
                    onNavigateToCalendar = { navController.navigate(Screen.Calendar.route) }
                )
            }
            
            composable(Screen.Calendar.route) {
                CalendarSplitScreen(viewModel = viewModel)
            }
        }
    }
}
