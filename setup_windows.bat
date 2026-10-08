@echo off
setlocal
cd /d "%~dp0"

echo ======================================
echo OpenScore Converter v0.0.3 - Setup
echo ======================================

where py >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python launcher "py" not found.
    echo Install Python 3.12 from https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3.12 -m venv .venv
    if errorlevel 1 (
        echo Python 3.12 not found; trying an installed Python 3...
        py -3 -m venv .venv
        if errorlevel 1 goto failed
    )
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed

echo.
echo [OK] Setup completed. Run run_windows.bat to launch.
pause
exit /b 0

:failed
echo.
echo [ERROR] Installation failed. Python 3.11-3.14 and Internet access are needed.
pause
exit /b 1
