@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

set REPO_NAME=adder
set GITHUB_USER=acydyq
set REMOTE_URL=https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo ======= GITHUB PUSH SCRIPT =======

REM -- Check for Git
where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed.
    pause
    exit /b 1
)

REM -- Check for GitHub CLI
where gh >nul 2>&1
if errorlevel 1 (
    echo ERROR: GitHub CLI not found.
    pause
    exit /b 1
)

REM -- Check GH auth
gh auth status >nul 2>&1
if errorlevel 1 (
    echo Not authenticated. Logging in...
    gh auth login
)

REM -- Check if repo exists
gh repo view %GITHUB_USER%/%REPO_NAME% >nul 2>&1
if errorlevel 1 (
    echo Creating GitHub repo: %REPO_NAME%
    gh repo create %REPO_NAME% --public --confirm
) else (
    echo Repo already exists.
)

REM -- Init repo if needed
if not exist ".git" (
    git init
    git branch -M main
)

REM -- Add remote if not set
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin %REMOTE_URL%
)

REM -- Commit and push
git add .
set /p COMMIT_MSG="Enter commit message: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Auto commit
git commit -m "%COMMIT_MSG%"
git push -u origin main

echo.
echo ======= DONE =======
pause
