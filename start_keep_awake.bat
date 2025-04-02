@echo off
setlocal ENABLEEXTENSIONS
title Keep Awake Utility Launcher

:menu
cls
echo ========================================
echo         Keep Awake Utility Launcher
echo ========================================
echo.
echo 1. Launch GUI Version
echo 2. Launch Console Version (Interactive)
echo 3. Launch Console Version (Background / Non-Interactive)
echo 4. Exit
echo.
set /p choice=Enter your choice [1-4]: 

if "%choice%"=="1" goto launch_gui
if "%choice%"=="2" goto launch_console
if "%choice%"=="3" goto launch_background
if "%choice%"=="4" goto end

echo Invalid choice. Try again.
pause
goto menu

:check_python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.6 or higher.
    pause
    exit /b
)
goto :eof

:check_dependencies
echo Checking and installing required packages...
pip install --disable-pip-version-check --quiet psutil pillow pyautogui pystray >nul
goto :eof

:launch_gui
call :check_python
call :check_dependencies
python main.py --auto-start --max-timer
goto end

:launch_console
call :check_python
call :check_dependencies
python console_keep_awake.py
goto end

:launch_background
call :check_python
call :check_dependencies
REM Use pythonw to suppress terminal window
start "" pythonw console_keep_awake.py --auto-start --max-timer --non-interactive
echo Background console launched. Check system tray for icon.
timeout /t 3 >nul
goto end

:end
endlocal
