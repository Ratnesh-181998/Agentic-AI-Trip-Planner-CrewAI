# 🚀 Deployment Guide - Agentic AI Trip Planner

This guide will help you deploy the Agentic AI Trip Planner to Streamlit Cloud and set up Git LFS for large files.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Git LFS Setup](#git-lfs-setup)
3. [GitHub Upload](#github-upload)
4. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ Git installed on your system
- ✅ GitHub account created
- ✅ Git LFS installed (for files > 100MB)
- ✅ Streamlit Cloud account (free at streamlit.io)
- ✅ API keys ready (Groq, Google Gemini)

---

## Git LFS Setup

Git LFS (Large File Storage) is required for files larger than 100MB. GitHub has a 100MB file size limit, but with LFS you can store files up to 2GB.

### Step 1: Install Git LFS

**Windows:**
```powershell
# Download from https://git-lfs.github.com/
# Or use Chocolatey
choco install git-lfs
```

**macOS:**
```bash
brew install git-lfs
```

**Linux:**
```bash
sudo apt-get install git-lfs  # Ubuntu/Debian
sudo yum install git-lfs      # CentOS/RHEL
```

### Step 2: Initialize Git LFS

```bash
cd "c:\Users\rattu\Downloads\AI Power Trip Planer Using CrewAI"
git lfs install
```

### Step 3: Track Large Files

The `.gitattributes` file is already configured to track:
- Images: `*.png`, `*.jpg`, `*.jpeg`, `*.gif`
- Videos: `*.mp4`, `*.mov`, `*.avi`
- Data files: `*.csv`, `*.db`, `*.sqlite`
- Models: `*.pkl`, `*.h5`, `*.pt`

Verify tracking:
```bash
git lfs track
```

---

## GitHub Upload

### Step 1: Initialize Git Repository

```bash
cd "c:\Users\rattu\Downloads\AI Power Trip Planer Using CrewAI"

# Initialize git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git
```

### Step 2: Stage All Files

```bash
# Add all files
git add .

# Check what will be committed
git status
```

### Step 3: Commit Changes

```bash
git commit -m "Initial commit: Agentic AI Trip Planner with 5-Tier Fallback System"
```

### Step 4: Push to GitHub

```bash
# Push to main branch
git push -u origin main

# If you get an error about existing repository, force push (CAREFUL!)
# git push -u origin main --force
```

### Step 5: Verify Upload

1. Go to https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI
2. Check that all files are uploaded
3. Verify LFS files show correct size (not just pointers)

---

## Streamlit Cloud Deployment

### Step 1: Sign Up for Streamlit Cloud

1. Visit https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### Step 2: Create New App

1. Click **"New app"** button
2. Select your repository: `Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI`
3. Select branch: `main`
4. Set main file path: `ratnesh_app_ULTIMATE.py`
5. Click **"Advanced settings"** (IMPORTANT!)

### Step 3: Configure Advanced Settings

**Python Version:**
- Select: `3.10` or `3.11`

**Secrets (Environment Variables):**
Click "Secrets" and add:

```toml
# Required API Keys
GROQ_API_KEY = "your_groq_api_key_here"
GOOGLE_API_KEY = "your_google_api_key_here"

# Optional API Keys
SERPER_API_KEY = "your_serper_api_key_here"
BROWSERLESS_API_KEY = "your_browserless_api_key_here"

# Ollama Configuration (if using)
OLLAMA_HOST = "http://localhost:11434"
```

**Resource Settings:**
- Memory: 2GB (recommended)
- CPU: 1 core (default)

### Step 4: Deploy

1. Click **"Deploy!"** button
2. Wait for deployment (usually 2-5 minutes)
3. Watch the build logs for any errors

### Step 5: Verify Deployment

1. Once deployed, you'll get a URL like: `https://agentic-ai-trip-planner-crewai.streamlit.app/`
2. Test all features:
   - ✅ AI Trip Planner generates itineraries
   - ✅ Flight/Hotel/Train/Bus search works
   - ✅ History tabs load correctly
   - ✅ Images display properly
   - ✅ 5-Tier Fallback System activates on errors

---

## Environment Variables

### Required Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `GROQ_API_KEY` | Groq LLM API key (Tier 1-3) | [console.groq.com](https://console.groq.com/) |
| `GOOGLE_API_KEY` | Google Gemini API key (Tier 4) | [makersuite.google.com](https://makersuite.google.com/app/apikey) |

### Optional Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `SERPER_API_KEY` | Advanced Google search | [serper.dev](https://serper.dev/) |
| `BROWSERLESS_API_KEY` | Web scraping | [browserless.io](https://www.browserless.io/) |
| `OLLAMA_HOST` | Local Ollama server | Install Ollama locally |

### How to Add Secrets on Streamlit Cloud

1. Go to your app dashboard
2. Click **"⚙️ Settings"**
3. Navigate to **"Secrets"** tab
4. Paste your secrets in TOML format
5. Click **"Save"**
6. App will automatically restart

---

## Troubleshooting

### Issue 1: "File too large" Error

**Problem:** Git rejects files > 100MB

**Solution:**
```bash
# Ensure Git LFS is installed and initialized
git lfs install

# Track large files
git lfs track "*.png" "*.jpg" "*.mp4"

# Add .gitattributes
git add .gitattributes

# Commit and push
git commit -m "Add Git LFS tracking"
git push
```

### Issue 2: "Module not found" on Streamlit Cloud

**Problem:** Missing dependencies

**Solution:**
1. Check `requirements.txt` is complete
2. Verify all imports are listed
3. Ensure version compatibility
4. Redeploy the app

### Issue 3: API Key Errors

**Problem:** "Invalid API key" or "Unauthorized"

**Solution:**
1. Verify API keys are correct in Streamlit Secrets
2. Check for extra spaces or newlines
3. Ensure keys are active and not expired
4. Test keys locally first

### Issue 4: App Crashes on Startup

**Problem:** App shows error on load

**Solution:**
1. Check deployment logs in Streamlit Cloud
2. Look for Python errors or missing files
3. Verify all required files are in repository
4. Check Python version compatibility (use 3.10 or 3.11)

### Issue 5: Images Not Loading

**Problem:** Destination images show broken links

**Solution:**
1. Verify images are in `images/` folder
2. Check Git LFS uploaded images correctly
3. Ensure image paths in code are correct
4. Test image URLs in browser

### Issue 6: 5-Tier Fallback Not Working

**Problem:** App fails instead of falling back

**Solution:**
1. Ensure both GROQ_API_KEY and GOOGLE_API_KEY are set
2. Check API key quotas aren't exceeded
3. Verify internet connectivity
4. Enable Ollama fallback if needed

---

## Post-Deployment Checklist

After successful deployment, verify:

- [ ] App loads without errors
- [ ] All tabs are accessible
- [ ] AI Trip Planner generates itineraries
- [ ] Flight/Hotel/Train/Bus search works
- [ ] History tabs display saved searches
- [ ] Images and videos load correctly
- [ ] 5-Tier Fallback System activates on errors
- [ ] Sidebar settings work properly
- [ ] Download buttons function correctly
- [ ] Mobile responsiveness works

---

## Updating the Deployed App

To update your deployed app:

```bash
# Make changes to your code
# ...

# Stage changes
git add .

# Commit
git commit -m "Update: Description of changes"

# Push to GitHub
git push origin main

# Streamlit Cloud will auto-deploy within 1-2 minutes
```

---

## Performance Optimization

### For Faster Loading:

1. **Optimize Images:**
   ```bash
   # Use compressed images
   # Recommended: PNG < 500KB, JPG < 200KB
   ```

2. **Cache Functions:**
   ```python
   @st.cache_data
   def expensive_function():
       # Your code here
   ```

3. **Lazy Loading:**
   - Load images only when tabs are opened
   - Use pagination for large lists

4. **CDN for Static Assets:**
   - Host large media files on CDN
   - Use URLs instead of local files

---

## Monitoring & Analytics

### Streamlit Cloud Analytics

1. Go to app dashboard
2. Click **"Analytics"** tab
3. View:
   - Daily active users
   - Session duration
   - Error rates
   - Resource usage

### Custom Logging

Add logging to track usage:

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info(f"User generated trip plan for {destination}")
```

---

## Security Best Practices

1. **Never commit API keys to Git**
   - Always use `.env` or Streamlit Secrets
   - Add `.env` to `.gitignore`

2. **Rotate API keys regularly**
   - Update keys every 90 days
   - Revoke old keys immediately

3. **Monitor API usage**
   - Set up alerts for unusual activity
   - Track daily/monthly quotas

4. **Use HTTPS only**
   - Streamlit Cloud provides HTTPS by default
   - Never use HTTP for API calls

---

## Support & Resources

- 📖 **Streamlit Docs**: https://docs.streamlit.io/
- 🐙 **Git LFS Docs**: https://git-lfs.github.com/
- 💬 **Streamlit Forum**: https://discuss.streamlit.io/
- 🐛 **Report Issues**: https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues

---

## Contact

For deployment help, contact:

**Ratnesh Singh**
- 📧 Email: rattudacsit2021gate@gmail.com
- 💼 LinkedIn: [linkedin.com/in/ratneshkumar1998](https://www.linkedin.com/in/ratneshkumar1998/)
- 🐙 GitHub: [github.com/Ratnesh-181998](https://github.com/Ratnesh-181998)

---

**Last Updated:** December 2024  
**Version:** 1.0
