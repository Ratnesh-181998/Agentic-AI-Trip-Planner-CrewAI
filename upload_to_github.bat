@echo off
echo ========================================
echo GitHub Upload Script
echo ========================================
echo.
echo This script will help you upload your project to GitHub.
echo.
echo STEP 1: You need a GitHub Personal Access Token
echo.
echo To create one:
echo 1. Visit: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Name it: "AI Trip Planner Upload"
echo 4. Select scope: repo (full control)
echo 5. Click "Generate token"
echo 6. COPY THE TOKEN
echo.
echo ========================================
echo.
set /p TOKEN="Paste your GitHub token here and press Enter: "
echo.
echo Uploading to GitHub...
echo.

git push https://%TOKEN%@github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Your project is now on GitHub!
    echo ========================================
    echo.
    echo Visit: https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI
    echo.
) else (
    echo.
    echo ========================================
    echo Upload failed. Please check your token.
    echo ========================================
    echo.
)

pause
