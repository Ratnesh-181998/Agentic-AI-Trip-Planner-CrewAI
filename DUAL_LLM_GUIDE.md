# 🤖 Dual LLM System - Groq + Ollama

## Overview

Your AI Trip Planner now supports **two LLM providers** with intelligent automatic fallback:

1. **Groq** (Cloud-based) - ⚡ Fast (30-90 seconds)
2. **Ollama** (Local) - 🐌 Slower (5-15 minutes) but offline

---

## 🎯 How It Works

### **Auto Mode (Default - Recommended)**
```
Try Groq → If fails → Switch to Ollama
```

**When Groq fails:**
- ❌ API key invalid/missing
- ❌ Rate limit exceeded
- ❌ Quota exhausted
- ❌ Network issues
- ❌ Service unavailable

**Automatic fallback to Ollama ensures:**
- ✅ Your app always works
- ✅ No manual intervention needed
- ✅ Seamless user experience

---

## 🎛️ Three Modes Available

### 1. **Auto (Groq → Ollama)** ⭐ Recommended
- Tries Groq first (fast)
- Falls back to Ollama if Groq fails
- Best of both worlds

### 2. **Groq Only**
- Only uses Groq API
- Fastest option
- Requires valid API key
- Fails if quota exhausted

### 3. **Ollama Only**
- Only uses local Ollama
- Works offline
- Slower but reliable
- Requires Ollama running locally

---

## 📋 Setup Instructions

### Option 1: Use Groq (Fast - Recommended)

1. **Get Free API Key**
   - Visit: https://console.groq.com/keys
   - Sign up (free)
   - Create API key

2. **Set API Key**
   
   **Method A: Environment Variable** (Recommended)
   ```powershell
   # Windows PowerShell
   $env:GROQ_API_KEY="gsk_your_key_here"
   ```
   
   **Method B: Direct in Code**
   - Edit `TravelAgents.py` line 16
   - Replace with your API key

3. **Run App**
   ```bash
   streamlit run my_app_2.py
   ```

### Option 2: Use Ollama (Offline)

1. **Install Ollama**
   - Download: https://ollama.ai/download
   - Install for your OS

2. **Pull Model**
   ```bash
   ollama pull llama3.2
   ```

3. **Start Ollama Server**
   ```bash
   ollama serve
   ```

4. **Run App**
   ```bash
   streamlit run my_app_2.py
   ```

### Option 3: Use Both (Auto Fallback) ⭐

1. Follow both setup instructions above
2. The app will automatically use Groq first
3. Falls back to Ollama if Groq fails

---

## 🎨 UI Controls

In the Streamlit sidebar, you can:

1. **Choose LLM Provider**
   - Auto (Groq → Ollama)
   - Groq Only
   - Ollama Only

2. **View Speed Comparison**
   - Groq: ~30-90 seconds
   - Ollama: ~5-15 minutes

3. **See Current Status**
   - Active provider
   - Warnings/info messages

---

## 🔧 Technical Details

### File: `TravelAgents.py`

```python
def get_llm(force_groq=False, force_ollama=False):
    """
    Smart LLM selector with automatic fallback
    
    Args:
        force_groq: Only use Groq (no fallback)
        force_ollama: Only use Ollama (skip Groq)
    
    Returns:
        LLM instance (Groq or Ollama)
    """
```

### Fallback Logic

```
1. Check force_ollama flag
   ├─ Yes → Use Ollama
   └─ No → Continue

2. Try Groq initialization
   ├─ Success → Return Groq LLM
   └─ Failure → Continue

3. Check force_groq flag
   ├─ Yes → Raise error (no fallback)
   └─ No → Continue

4. Try Ollama initialization
   ├─ Success → Return Ollama LLM
   └─ Failure → Return Groq (last resort)
```

---

## 📊 Performance Comparison

| Feature | Groq | Ollama |
|---------|------|--------|
| **Speed** | ⚡ 30-90 sec | 🐌 5-15 min |
| **Cost** | 🆓 Free (with limits) | 🆓 Free |
| **Internet** | ✅ Required | ❌ Not required |
| **Setup** | Easy (API key) | Medium (install) |
| **Reliability** | High (99.9% uptime) | Very High (local) |
| **Privacy** | Cloud-based | 100% Local |

---

## 🆘 Troubleshooting

### Groq Issues

**Error: "Invalid API Key"**
```bash
# Check your API key
echo $env:GROQ_API_KEY  # Windows PowerShell
```

**Error: "Rate Limit Exceeded"**
- Wait a few minutes
- App will auto-switch to Ollama
- Or manually select "Ollama Only"

**Error: "Quota Exhausted"**
- Groq free tier: 14,400 requests/day
- App will auto-switch to Ollama
- Or wait 24 hours for reset

### Ollama Issues

**Error: "Connection refused"**
```bash
# Make sure Ollama is running
ollama serve
```

**Error: "Model not found"**
```bash
# Pull the model
ollama pull llama3.2
```

**Error: "Ollama not installed"**
- Download from: https://ollama.ai/download
- Install and restart terminal

---

## 🎯 Best Practices

### For Development
- Use **Auto mode** for best experience
- Groq for speed, Ollama as backup

### For Production
- Use **Groq Only** with monitoring
- Set up quota alerts
- Have Ollama ready as backup

### For Offline Use
- Use **Ollama Only**
- Pre-pull required models
- Ensure sufficient RAM (8GB+)

---

## 📈 Monitoring

### Check Active LLM

The console will show:
```
🚀 Attempting to use Groq LLM (fast cloud-based)...
✅ Groq LLM initialized successfully!
```

Or:
```
⚠️ Groq LLM failed: Rate limit exceeded
🔄 Falling back to local Ollama LLM...
✅ Ollama LLM initialized successfully!
```

---

## 🔐 Security Notes

### Groq API Key
- Never commit API keys to Git
- Use environment variables
- Rotate keys regularly
- Monitor usage at: https://console.groq.com/

### Ollama
- Runs locally (no data sent to cloud)
- Full privacy control
- No API key needed

---

## 📞 Support

- **Groq**: https://console.groq.com/docs
- **Ollama**: https://ollama.ai/docs
- **CrewAI**: https://docs.crewai.com/

---

## ✅ Summary

Your app now has:
- ✅ Dual LLM support (Groq + Ollama)
- ✅ Automatic fallback system
- ✅ UI controls for manual selection
- ✅ Detailed logging and status
- ✅ Error handling and recovery
- ✅ Works online and offline

**Result**: A robust, fast, and reliable AI Trip Planner! 🚀
