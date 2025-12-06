#!/usr/bin/env python3
"""
Security Check Script
Verifies that no sensitive information is in the codebase before pushing to GitHub
"""

import os
import re
from pathlib import Path

def check_for_api_keys(directory="."):
    """Check for hardcoded API keys in Python files"""
    
    # Pattern to match Groq API keys
    api_key_pattern = re.compile(r'gsk_[a-zA-Z0-9]{48,}')
    
    issues = []
    python_files = Path(directory).rglob("*.py")
    
    for file_path in python_files:
        # Skip virtual environment and cache directories
        if '.venv' in str(file_path) or '__pycache__' in str(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for API keys
                matches = api_key_pattern.findall(content)
                if matches:
                    issues.append(f"⚠️  FOUND API KEY in {file_path}")
                    
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return issues

def check_gitignore():
    """Verify .gitignore has necessary entries"""
    
    required_entries = ['.env', '.env.local', '*.log', '__pycache__']
    
    if not os.path.exists('.gitignore'):
        return ["❌ .gitignore file not found!"]
    
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    missing = []
    for entry in required_entries:
        if entry not in gitignore_content:
            missing.append(f"⚠️  Missing in .gitignore: {entry}")
    
    return missing

def check_env_files():
    """Check if .env.example exists and .env is not tracked"""
    
    issues = []
    
    if not os.path.exists('.env.example'):
        issues.append("⚠️  .env.example not found (should exist as template)")
    
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as f:
            content = f.read()
            if 'gsk_' in content and len(content.split('gsk_')[1][:10]) > 10:
                issues.append("❌ .env.example contains real API key!")
    
    return issues

def main():
    print("=" * 70)
    print("🔒 SECURITY CHECK - Pre-GitHub Push Verification")
    print("=" * 70)
    print()
    
    all_issues = []
    
    # Check 1: Hardcoded API keys
    print("📝 Checking for hardcoded API keys...")
    api_key_issues = check_for_api_keys()
    if api_key_issues:
        all_issues.extend(api_key_issues)
    else:
        print("✅ No hardcoded API keys found")
    print()
    
    # Check 2: .gitignore
    print("📝 Checking .gitignore...")
    gitignore_issues = check_gitignore()
    if gitignore_issues:
        all_issues.extend(gitignore_issues)
    else:
        print("✅ .gitignore looks good")
    print()
    
    # Check 3: Environment files
    print("📝 Checking environment files...")
    env_issues = check_env_files()
    if env_issues:
        all_issues.extend(env_issues)
    else:
        print("✅ Environment files configured correctly")
    print()
    
    # Summary
    print("=" * 70)
    if all_issues:
        print("❌ SECURITY ISSUES FOUND:")
        print("=" * 70)
        for issue in all_issues:
            print(issue)
        print()
        print("⚠️  DO NOT push to GitHub until these issues are resolved!")
        return 1
    else:
        print("✅ ALL SECURITY CHECKS PASSED!")
        print("=" * 70)
        print()
        print("🚀 Safe to push to GitHub!")
        print()
        print("Next steps:")
        print("  1. git add .")
        print("  2. git commit -m 'Your message'")
        print("  3. git push origin main")
        return 0

if __name__ == "__main__":
    exit(main())
