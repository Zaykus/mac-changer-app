@echo off
setlocal

:: Change to the directory of this script
cd /d "%~dp0"

echo Current directory: %cd%
echo Listing files:
dir /b

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Run the Python GUI (prefer venv, fallback to system Python)
if exist "venv\Scripts\python.exe" (
    echo Using venv Python...
    venv\Scripts\python.exe run_mac_changer_gui.py
) else (
    echo Using system Python...
    python run_mac_changer_gui.py
)

pause
