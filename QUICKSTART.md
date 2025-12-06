# 🚀 Quick Start Guide

Get the Agentic AI Trip Planner running in 5 minutes!

## ⚡ Fast Setup (Local)

### 1. Clone Repository
```bash
git clone https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git
cd Agentic-AI-Trip-Planner-CrewAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
```

**Get Free API Keys:**
- Groq: https://console.groq.com/
- Google: https://makersuite.google.com/app/apikey

### 4. Run the App
```bash
streamlit run ratnesh_app_ULTIMATE.py
```

Open http://localhost:8501 in your browser!

---

## 🌐 Use Online (No Installation)

Visit the live demo: **[Streamlit App](https://agentic-ai-trip-planner-crewai.streamlit.app/)**

---

## 🎯 First Trip Plan

1. **Select Locations**: Choose from/to country and city
2. **Set Dates**: Pick departure and return dates
3. **Add Travelers**: Enter number of adults and children
4. **Choose Interests**: Select from 24+ travel interests
5. **Generate**: Click "🚀 Generate Travel Plan"
6. **Wait**: AI agents will create your itinerary (1-2 minutes)
7. **Review**: Get detailed day-by-day plan with budget

---

## 🔧 Troubleshooting

**Issue: "Module not found"**
```bash
pip install --upgrade -r requirements.txt
```

**Issue: "API key invalid"**
- Check `.env` file has correct keys
- Verify no extra spaces or quotes
- Test keys at provider websites

**Issue: "Rate limit exceeded"**
- The 5-Tier Fallback System will auto-switch providers
- Wait a few minutes and try again
- Or use "Google Only" mode in sidebar

---

## 📚 Learn More

- [Full README](README.md) - Complete documentation
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Deploy to cloud
- [GitHub Issues](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues) - Report bugs

---

## 💡 Pro Tips

1. **Use Auto Mode**: Let the 5-Tier Fallback System handle provider selection
2. **Save History**: All plans auto-save to `trip_plans/` folder
3. **Explore Interests**: Check "Explore by Interest" tab for inspiration
4. **Download Plans**: Export any itinerary as TXT file
5. **Multi-Interest**: Select multiple interests for better recommendations

---

**Need Help?** Contact: rattudacsit2021gate@gmail.com
