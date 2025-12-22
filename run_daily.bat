@echo off
cd /d "%~dp0"
echo "Starting PyDaily Morning Cycle..."
python run_bot.py --mode morning
echo "Waiting for Evening Cycle (Simulated for Batch)..."
:: In reality, you'd schedule two separate tasks. 
:: This script is just a helper to test or run one mode.
:: To run evening, change typical usage to: python run_bot.py --mode evening
pause
