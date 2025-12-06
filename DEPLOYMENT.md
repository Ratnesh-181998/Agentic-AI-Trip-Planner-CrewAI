# 🚀 Deployment Guide - GitHub & Streamlit Cloud

## 📋 Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [GitHub Deployment](#github-deployment)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Environment Variables](#environment-variables)
5. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

**Option A: Using .env file** (Recommended)
```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your API key
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Option B: Set Environment Variable**
```powershell
# Windows PowerShell
$env:GROQ_API_KEY="gsk_your_api_key_here"

# Windows CMD
set GROQ_API_KEY=gsk_your_api_key_here

# Linux/Mac
export GROQ_API_KEY="gsk_your_api_key_here"
```

### Step 5: Run the App
```bash
streamlit run my_app_2.py
```

---

## 🐙 GitHub Deployment

### Step 1: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: AI Trip Planner"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., `ai-trip-planner`)
3. **DO NOT** initialize with README (you already have one)

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/your-username/ai-trip-planner.git
git branch -M main
git push -u origin main
```

### ⚠️ Security Checklist

Before pushing, ensure:
- ✅ `.env` is in `.gitignore`
- ✅ No API keys in code
- ✅ `.env.example` has placeholder values only
- ✅ Sensitive files are not tracked

**Verify with:**
```bash
git status  # Should NOT show .env file
```

---

## ☁️ Streamlit Cloud Deployment

### Step 1: Sign Up for Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Authorize Streamlit to access your repositories

### Step 2: Deploy App
1. Click **"New app"**
2. Select your repository: `your-username/ai-trip-planner`
3. Choose branch: `main`
4. Set main file path: `my_app_2.py`
5. Click **"Deploy!"**

### Step 3: Configure Secrets (Environment Variables)

**IMPORTANT**: Add your API key as a secret in Streamlit Cloud

1. In your deployed app, click **⚙️ Settings** (top right)
2. Go to **"Secrets"** section
3. Add your environment variables:

```toml
# .streamlit/secrets.toml format
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```

4. Click **"Save"**
5. App will automatically restart

### Step 4: Access Your App
Your app will be available at:
```
https://your-username-ai-trip-planner-main-my-app-2.streamlit.app
```

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Where to Get | Required |
|----------|-------------|--------------|----------|
| `GROQ_API_KEY` | Groq API key for fast LLM | https://console.groq.com/keys | No* |

*Not required if using Ollama only mode

### How to Set Variables

#### Local Development
```bash
# .env file (recommended)
GROQ_API_KEY=gsk_your_key_here

# Or environment variable
export GROQ_API_KEY="gsk_your_key_here"
```

#### Streamlit Cloud
```toml
# Settings → Secrets
GROQ_API_KEY = "gsk_your_key_here"
```

#### GitHub Actions (if using CI/CD)
```yaml
# .github/workflows/deploy.yml
env:
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

---

## 🔧 Configuration Files

### `.gitignore`
Already configured to exclude:
- ✅ `.env` files
- ✅ `__pycache__/`
- ✅ `.venv/`
- ✅ `.streamlit/`
- ✅ `*.log`

### `requirements.txt`
All dependencies are listed. Streamlit Cloud will automatically install them.

### `.env.example`
Template file (safe to commit):
```bash
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'crewai'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "GROQ_API_KEY not found"
**Solution:**
- **Local**: Create `.env` file with your API key
- **Streamlit Cloud**: Add secret in Settings → Secrets

### Issue: "Ollama connection refused"
**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# Pull the model
ollama pull llama3.2
```

### Issue: App uses Ollama instead of Groq
**Possible causes:**
1. API key not set correctly
2. Groq quota exhausted (check https://console.groq.com/)
3. Network issues

**Check console output:**
```
🚀 Attempting to use Groq LLM...
⚠️ Groq LLM failed: [error message]
🔄 Falling back to Ollama...
```

### Issue: "Rate limit exceeded" on Groq
**Solution:**
- App will automatically switch to Ollama
- Or wait for quota reset (24 hours)
- Or upgrade Groq plan

### Issue: Streamlit Cloud deployment fails
**Common fixes:**
1. Check `requirements.txt` is complete
2. Verify main file path is `my_app_2.py`
3. Check app logs in Streamlit Cloud dashboard
4. Ensure secrets are set correctly

---

## 📊 Deployment Checklist

### Before Pushing to GitHub
- [ ] Remove all hardcoded API keys
- [ ] Create `.env.example` with placeholders
- [ ] Verify `.gitignore` includes `.env`
- [ ] Test app locally
- [ ] Update README.md
- [ ] Check `requirements.txt` is complete

### Before Deploying to Streamlit Cloud
- [ ] Push code to GitHub
- [ ] Create Streamlit Cloud account
- [ ] Add GROQ_API_KEY to Secrets
- [ ] Test deployment
- [ ] Verify app works in cloud
- [ ] Share public URL

---

## 🌐 Public vs Private Repository

### Public Repository (Recommended for Portfolio)
- ✅ Showcase your work
- ✅ Free Streamlit Cloud hosting
- ⚠️ **NEVER** commit API keys
- ⚠️ Use environment variables only

### Private Repository
- ✅ Keep code private
- ✅ Still use environment variables
- ⚠️ May require paid Streamlit plan

---

## 📝 Best Practices

### Security
1. **Never** commit `.env` files
2. **Always** use environment variables for secrets
3. **Rotate** API keys regularly
4. **Monitor** API usage

### Code Management
1. Use meaningful commit messages
2. Create branches for features
3. Test before pushing
4. Keep dependencies updated

### Deployment
1. Test locally first
2. Use staging environment
3. Monitor app logs
4. Set up error tracking

---

## 🔗 Useful Links

- **Groq Console**: https://console.groq.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Docs**: https://docs.github.com/
- **Streamlit Cloud**: https://streamlit.io/cloud

---

## 📞 Support

### Getting Help
1. Check this guide first
2. Review error messages in console
3. Check Streamlit Cloud logs
4. Search GitHub issues
5. Ask in Streamlit Community Forum

### Reporting Issues
When reporting issues, include:
- Error message
- Steps to reproduce
- Environment (local/cloud)
- Python version
- Dependencies versions

---

## ✅ Quick Reference

### Local Development
```bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API key

# Run
streamlit run my_app_2.py
```

### GitHub Push
```bash
git add .
git commit -m "Your message"
git push origin main
```

### Streamlit Cloud
1. Connect GitHub repo
2. Set main file: `my_app_2.py`
3. Add secrets: `GROQ_API_KEY`
4. Deploy!

---

**Your app is now ready for deployment! 🚀**
