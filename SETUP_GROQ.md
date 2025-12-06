# 🚀 Speed Up Your AI Trip Planner with Groq

## Why Switch to Groq?

Your app was using **Ollama (local LLM)** which is slow because:
- Runs on your local machine (CPU/GPU limited)
- Each agent call takes 30-60+ seconds
- Total time: 5-15 minutes per trip plan

**Groq** is a cloud-based LLM that's:
- ⚡ **10-20x faster** than local Ollama
- 🆓 **Free** to use (with generous limits)
- 🎯 **More reliable** and consistent

Expected time with Groq: **30-90 seconds** per trip plan!

---

## 📝 Setup Instructions

### Step 1: Get Your Free Groq API Key

1. Go to: **https://console.groq.com/keys**
2. Sign up for a free account (if you don't have one)
3. Click **"Create API Key"**
4. Copy your API key (starts with `gsk_...`)

### Step 2: Set Your API Key

You have **two options**:

#### Option A: Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your-api-key-here"

# Windows CMD
set GROQ_API_KEY=your-api-key-here

# Linux/Mac
export GROQ_API_KEY="your-api-key-here"
```

#### Option B: Direct in Code
Edit `TravelAgents.py` line 9:
```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_your_actual_api_key_here")
```

### Step 3: Install Groq Package
```bash
pip install groq
```

### Step 4: Run Your App
```bash
streamlit run my_app_2.py
```

---

## 🔄 Switch Back to Ollama (If Needed)

If you want to use Ollama again, edit `TravelAgents.py`:

```python
# Replace this:
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY
)

# With this:
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)
```

---

## 📊 Performance Comparison

| LLM Provider | Average Time | Cost |
|--------------|-------------|------|
| Ollama (Local) | 5-15 minutes | Free |
| **Groq (Cloud)** | **30-90 seconds** | **Free** |
| OpenAI GPT-4 | 1-2 minutes | Paid |

---

## ✅ What Was Changed

1. **TravelAgents.py**: Switched from Ollama to Groq LLM
2. **requirements.txt**: Added `groq>=0.4.0`
3. All three agents now use the faster Groq API

---

## 🆘 Troubleshooting

### Error: "Invalid API Key"
- Make sure you copied the full API key (starts with `gsk_`)
- Check that the environment variable is set correctly

### Error: "Rate Limit Exceeded"
- Groq free tier has limits (14,400 requests/day)
- Wait a few minutes and try again

### Still Slow?
- Check your internet connection
- Verify the API key is working
- Check Groq status: https://status.groq.com/

---

## 📞 Support

- Groq Documentation: https://console.groq.com/docs
- Groq Discord: https://discord.gg/groq
