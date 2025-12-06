# 📤 GitHub Upload Instructions

Follow these steps to upload your project to GitHub.

## 📋 Prerequisites

- ✅ Git installed on your system
- ✅ GitHub account created
- ✅ Repository created: `Agentic-AI-Trip-Planner-CrewAI`
- ✅ Git LFS installed (for large files)

---

## 🚀 Step-by-Step Upload Process

### Step 1: Configure Git (First Time Only)

```bash
# Set your name and email
git config --global user.name "Ratnesh Singh"
git config --global user.email "rattudacsit2021gate@gmail.com"

# Verify configuration
git config --list
```

### Step 2: Navigate to Project Directory

```bash
cd "c:\Users\rattu\Downloads\AI Power Trip Planer Using CrewAI"
```

### Step 3: Check Git Status

```bash
# See what files will be uploaded
git status

# Should show:
# - Modified: README.md, requirements.txt, .gitignore
# - New files: .gitattributes, DEPLOYMENT_GUIDE.md, QUICKSTART.md
```

### Step 4: Stage All Files

```bash
# Add all files to staging
git add .

# Verify what's staged
git status
```

### Step 5: Commit Changes

```bash
# Commit with descriptive message
git commit -m "Initial commit: Agentic AI Trip Planner with comprehensive documentation

- Added 5-Tier Fallback System for 99.9% uptime
- Implemented multi-agent AI system with CrewAI
- Created comprehensive README with all features
- Added deployment guide for Streamlit Cloud
- Configured Git LFS for large files
- Included quick start guide for users
- Set up proper .gitignore and .gitattributes"
```

### Step 6: Push to GitHub

```bash
# Push to main branch
git push -u origin main
```

**If you get an error about existing content:**

```bash
# Option 1: Pull first, then push
git pull origin main --allow-unrelated-histories
git push -u origin main

# Option 2: Force push (CAUTION: This will overwrite remote)
git push -u origin main --force
```

### Step 7: Verify Upload

1. Go to: https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI
2. Check all files are present
3. Verify README displays correctly
4. Check images are uploaded via Git LFS

---

## 🔍 Verification Checklist

After upload, verify:

- [ ] README.md displays with proper formatting
- [ ] All Python files are present
- [ ] Images in `images/` folder are accessible
- [ ] `.env.example` is present (but NOT `.env`)
- [ ] `requirements.txt` is complete
- [ ] `.gitignore` is working (no `.env`, `__pycache__`, etc.)
- [ ] `.gitattributes` is configured for Git LFS
- [ ] All documentation files are readable

---

## 📁 Files That Should Be Uploaded

### Core Application Files
- ✅ `ratnesh_app_ULTIMATE.py` - Main application
- ✅ `TravelAgents.py` - AI agent definitions
- ✅ `TravelTasks.py` - Task definitions
- ✅ `TravelTasks_LEGACY.py` - Legacy tasks
- ✅ `TravelTools.py` - Search tools

### Configuration Files
- ✅ `requirements.txt` - Dependencies
- ✅ `.env.example` - Environment template
- ✅ `.gitignore` - Git exclusions
- ✅ `.gitattributes` - Git LFS config

### Documentation Files
- ✅ `README.md` - Main documentation
- ✅ `DEPLOYMENT_GUIDE.md` - Deployment instructions
- ✅ `QUICKSTART.md` - Quick start guide
- ✅ All other `.md` files in root

### Data & Assets
- ✅ `images/` folder - Destination images
- ✅ Sample trip plans (optional)
- ✅ Sample search history (optional)

---

## 🚫 Files That Should NOT Be Uploaded

These are automatically excluded by `.gitignore`:

- ❌ `.env` - Your API keys (NEVER upload!)
- ❌ `__pycache__/` - Python cache
- ❌ `.venv/` - Virtual environment
- ❌ `*.log` - Log files
- ❌ `.vscode/` - IDE settings
- ❌ `.DS_Store` - macOS files

---

## 🔐 Security Check

**CRITICAL: Before pushing, ensure:**

1. **No API keys in code**
   ```bash
   # Search for potential API keys
   grep -r "GROQ_API_KEY" --include="*.py" .
   grep -r "GOOGLE_API_KEY" --include="*.py" .
   ```
   
   Should only find references in comments or `.env.example`

2. **`.env` is ignored**
   ```bash
   git status | grep ".env"
   ```
   
   Should show nothing (`.env` should be ignored)

3. **Secrets not in history**
   ```bash
   git log --all --full-history --source -- .env
   ```
   
   Should show nothing

---

## 🔄 Updating Repository

After initial upload, to update:

```bash
# Make your changes
# ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Update: Description of changes"

# Push to GitHub
git push origin main
```

---

## 🌿 Branch Management (Optional)

For development workflow:

```bash
# Create development branch
git checkout -b development

# Make changes and commit
git add .
git commit -m "Feature: New feature description"

# Push development branch
git push -u origin development

# Merge to main when ready
git checkout main
git merge development
git push origin main
```

---

## 📊 Git LFS Verification

Check if large files are tracked by LFS:

```bash
# List LFS tracked files
git lfs ls-files

# Check LFS status
git lfs status

# Verify LFS is working
git lfs env
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Permission denied (publickey)"

**Solution:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "rattudacsit2021gate@gmail.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings > SSH and GPG keys > New SSH key
```

Or use HTTPS instead:
```bash
git remote set-url origin https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git
```

### Issue 2: "Large files detected"

**Solution:**
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.png" "*.jpg" "*.mp4"

# Add .gitattributes
git add .gitattributes

# Commit and push
git commit -m "Add Git LFS tracking"
git push
```

### Issue 3: "Repository not found"

**Solution:**
1. Verify repository exists on GitHub
2. Check repository name spelling
3. Ensure you have access permissions
4. Use correct remote URL

### Issue 4: "Failed to push some refs"

**Solution:**
```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Issue 5: "Accidentally committed .env file"

**Solution:**
```bash
# Remove from Git (but keep local file)
git rm --cached .env

# Add to .gitignore
echo ".env" >> .gitignore

# Commit the removal
git commit -m "Remove .env from tracking"

# Push
git push origin main

# IMPORTANT: Rotate all API keys immediately!
```

---

## 📞 Need Help?

If you encounter issues:

1. Check [GitHub Docs](https://docs.github.com/)
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/git)
3. Contact: rattudacsit2021gate@gmail.com

---

## ✅ Final Checklist

Before considering upload complete:

- [ ] All files uploaded successfully
- [ ] README displays correctly on GitHub
- [ ] No sensitive data (API keys, passwords) in repository
- [ ] `.gitignore` working properly
- [ ] Git LFS configured for large files
- [ ] Repository is public (or private, as intended)
- [ ] Repository description and topics added
- [ ] License file present (MIT)
- [ ] Repository URL shared: https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI

---

**Congratulations! Your project is now on GitHub! 🎉**

Next step: [Deploy to Streamlit Cloud](DEPLOYMENT_GUIDE.md)
