#!/bin/bash
# GitHub Upload Script for AI Trip Planner
# 
# INSTRUCTIONS:
# 1. Get your GitHub token from: https://github.com/settings/tokens/new
#    - Note: AI Trip Planner Upload
#    - Expiration: 90 days
#    - Scope: ✅ repo
# 2. Replace YOUR_GITHUB_TOKEN_HERE below with your actual token
# 3. Save this file
# 4. Run: bash upload.sh

# ============================================
# EDIT THIS LINE - Replace with your token:
GITHUB_TOKEN="YOUR_GITHUB_TOKEN_HERE"
# ============================================

echo "=========================================="
echo "Uploading AI Trip Planner to GitHub"
echo "=========================================="
echo ""

if [ "$GITHUB_TOKEN" = "YOUR_GITHUB_TOKEN_HERE" ]; then
    echo "❌ ERROR: Please edit this file and add your GitHub token!"
    echo ""
    echo "Get your token from: https://github.com/settings/tokens/new"
    echo ""
    exit 1
fi

echo "📦 Pushing to GitHub..."
echo ""

git push https://${GITHUB_TOKEN}@github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Project uploaded to GitHub!"
    echo "=========================================="
    echo ""
    echo "🌐 View your repository:"
    echo "https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI"
    echo ""
    echo "📋 Next steps:"
    echo "1. Visit your repository and verify files"
    echo "2. Deploy to Streamlit Cloud"
    echo "3. Share your project!"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Upload failed"
    echo "=========================================="
    echo ""
    echo "Please check:"
    echo "- Your token is correct"
    echo "- Token has 'repo' scope"
    echo "- You have internet connection"
    echo ""
fi
