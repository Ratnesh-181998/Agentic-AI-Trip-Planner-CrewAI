# PowerShell Upload Script for AI Trip Planner
# 
# INSTRUCTIONS:
# 1. Get your GitHub token from: https://github.com/settings/tokens/new
#    - Note: AI Trip Planner Upload
#    - Expiration: 90 days
#    - Scope: ✅ repo
# 2. Replace YOUR_GITHUB_TOKEN_HERE below with your actual token
# 3. Save this file
# 4. Right-click and select "Run with PowerShell"

# ============================================
# EDIT THIS LINE - Replace with your token:
$GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
# ============================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Uploading AI Trip Planner to GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($GITHUB_TOKEN -eq "YOUR_GITHUB_TOKEN_HERE") {
    Write-Host "❌ ERROR: Please edit this file and add your GitHub token!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Get your token from: https://github.com/settings/tokens/new" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "📦 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""

Set-Location "c:\Users\rattu\Downloads\AI Power Trip Planer Using CrewAI"

git push "https://$($GITHUB_TOKEN)@github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git" main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS! Project uploaded to GitHub!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 View your repository:" -ForegroundColor Cyan
    Write-Host "https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Visit your repository and verify files" -ForegroundColor White
    Write-Host "2. Deploy to Streamlit Cloud" -ForegroundColor White
    Write-Host "3. Share your project!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host "❌ Upload failed" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "- Your token is correct" -ForegroundColor White
    Write-Host "- Token has 'repo' scope" -ForegroundColor White
    Write-Host "- You have internet connection" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
