@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Universal Git Push Script with Timestamp and Optional Message

REM Step 1: Navigate to script directory
cd /d "%~dp0"

REM Step 2: Check if .git exists
IF NOT EXIST ".git" (
    echo Git repository not initialized.
    set /p INIT_REPO=Do you want to initialize this folder as a Git repo? (y/n): 
    if /I "!INIT_REPO!"=="Y" (
        git init
        echo # Auto-initialized repository> README.md
        git add .
        set /p REMOTE_URL=Enter remote origin URL: 
        git remote add origin !REMOTE_URL!
        git commit -m "Initial commit"
        git branch -M master
        git push -u origin master
    ) else (
        echo Aborting...
        exit /b
    )
) else (
    REM Step 3: Check for commit_message.txt
    if exist "commit_message.txt" (
        for /f "delims=" %%A in (commit_message.txt) do (
            set MSG=%%A
            goto :commit
        )
    ) else (
        REM Step 4: Ask for manual message if file not found
        set /p MSG=Enter commit message: 
    )

    :commit
    git add .
    git commit -m "!MSG! [%date% %time%]"
    git push
)

ENDLOCAL
pause