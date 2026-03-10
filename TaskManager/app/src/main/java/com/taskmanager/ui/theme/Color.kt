package com.taskmanager.ui.theme

import androidx.compose.ui.graphics.Color

// Google Core Inspired Accents
val BrandBlue = Color(0xFF4285F4)   // Active timers, primary actions
val BrandRed = Color(0xFFEA4335)    // High priority, destructive actions
val BrandYellow = Color(0xFFFBBC05) // Micro-repeating task indicators, warnings
val BrandGreen = Color(0xFF34A853)  // Completion states, success

// Default Light Colors (Fallback if Dynamic Color unavailable)
val LightPrimary = BrandBlue
val LightOnPrimary = Color.White
val LightBackground = Color(0xFFF8F9FA)
val LightSurface = Color.White
val LightOnSurface = Color(0xFF202124)

// Default Dark Colors (Fallback)
val DarkPrimary = Color(0xFF8AB4F8) 
val DarkOnPrimary = Color(0xFF202124)
val DarkBackground = Color(0xFF202124)
val DarkSurface = Color(0xFF303134)
val DarkOnSurface = Color(0xFFE8EAED)

// Glassmorphism alphas
const val GlassAlphaLight = 0.85f
const val GlassAlphaDark = 0.70f
