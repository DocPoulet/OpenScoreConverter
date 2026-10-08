@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Environment not found. Run setup_windows.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m openscore
if errorlevel 1 (
    echo.
    echo [ERROR] OpenScore Converter could not start.
    pause
    exit /b 1
)
