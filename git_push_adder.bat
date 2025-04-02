@echo off
setlocal ENABLEEXTENSIONS

REM === CONFIGURATION ===
set REPO_NAME=adder
set REMOTE_URL=https://github.com/acydyq/%REPO_NAME%.git

echo --------------------------------------------
echo      GitHub Auto-Commit & Push Script
echo      Project Name: %REPO_NAME%
echo --------------------------------------------

REM === CHECK FOR GIT ===
where git >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Git is not installed or not in PATH.
    echo Please install Git and try again.
    pause
    exit /b 1
)

REM === CHECK IF .git EXISTS ===
IF NOT EXIST ".git" (
    echo No Git repo found. Initializing new Git repo...
    git init
    echo # %REPO_NAME% > README.md
    git add .
    git commit -m "Initial commit for %REPO_NAME% project"
    git branch -M main
    git remote add origin %REMOTE_URL%
) ELSE (
    echo Git repository already initialized.
)

REM === CHECK IF REMOTE EXISTS ===
git remote get-url origin >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Setting remote origin to: %REMOTE_URL%
    git remote add origin %REMOTE_URL%
)

REM === COMMIT CHANGES ===
set /p COMMIT_MSG="Enter commit message: "
IF "%COMMIT_MSG%"=="" set COMMIT_MSG=Auto commit

git add .
git commit -m "%COMMIT_MSG%"
git push -u origin main

echo --------------------------------------------
echo Push to GitHub completed!
echo --------------------------------------------
pause
