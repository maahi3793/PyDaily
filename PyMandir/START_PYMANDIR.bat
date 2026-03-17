@echo off
title PyMandir - Temple of Knowledge
echo.
echo   =================================
echo        PyMandir - Starting...
echo   =================================
echo.
echo   Opening http://localhost:8080 in your browser...
echo.
start http://localhost:8080
npx -y http-server "c:\Users\reach\.gemini\antigravity\scratch\relaunchpython\PyMandir" -p 8080 -c-1
