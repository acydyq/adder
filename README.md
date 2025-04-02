@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM === GET CURRENT FOLDER NAME ===
for %%F in ("%CD%") do set REPO_NAME=%%~nxF

REM === CONFIGURATION ===
REM GitHub username will be auto-detected from gh auth
set REMOTE_URL=https://github.com/placeholder/%REPO_NAME%.git

REM === Get timestamp for commit message ===
for /f "tokens=1-2 delims= " %%a in ('wmic os get localdatetime ^| find "."') do (
    set DATETIME=%%a
)
set COMMIT_DATE=!DATETIME:~0,4!-!DATETIME:~4,2!-!DATETIME:~6,2!
set COMMIT_TIME=!DATETIME:~8,2!:!DATETIME:~10,2!:!DATETIME:~12,2!
set COMMIT_MSG=Auto commit - !COMMIT_DATE! !COMMIT_TIME!

echo.
echo ======= UNIVERSAL GITHUB PUSH SCRIPT =======
echo Project Folder: %REPO_NAME%
echo Commit Message: %COMMIT_MSG%
echo ===========================================

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

REM -- Detect GitHub username
for /f "tokens=2 delims=: " %%u in ('gh auth status') do (
    if not defined GITHUB_USER set GITHUB_USER=%%u
)
set REMOTE_URL=https://github.com/%GITHUB_USER%/%REPO_NAME%.git

REM -- Check if repo exists
gh repo view %GITHUB_USER%/%REPO_NAME% >nul 2>&1
if errorlevel 1 (
    echo 🆕 Creating GitHub repo: %REPO_NAME%
    gh repo create %REPO_NAME% --public --confirm
) else (
    echo ✅ Repo already exists on GitHub.
)

REM -- Init repo if needed
if not exist ".git" (
    echo 🧱 Initializing Git repo...
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
git commit -m "%COMMIT_MSG%" >nul 2>&1
git push -u origin main

echo.
echo ✅ Repo pushed to: %REMOTE_URL%
echo ===========================================
pause
