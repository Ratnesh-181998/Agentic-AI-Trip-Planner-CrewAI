# 🚀 Quick Start Guide - AI Trip Planner

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Using the Application](#using-the-application)
5. [Understanding the Logs](#understanding-the-logs)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Ollama**: [Download Ollama](https://ollama.ai/)
- **LLaMA 3.2 Model**: Install via Ollama

### Installing Ollama and LLaMA 3.2

1. **Install Ollama**:
   - Visit https://ollama.ai/
   - Download and install for your operating system
   - Follow the installation wizard

2. **Pull LLaMA 3.2 Model**:
   ```bash
   ollama pull llama3.2
   ```

3. **Start Ollama Server**:
   ```bash
   ollama serve
   ```
   Keep this terminal window open while using the app.

---

## Installation

### Step 1: Clone or Download the Project
```bash
cd "C:\Users\rattu\Downloads\AI Power Trip Planer Using CrewAI"
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Method 1: Using Streamlit Command
```bash
streamlit run app.py
```

### Method 2: Using Python
```bash
python -m streamlit run app.py
```

The application will automatically open in your default browser at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://192.168.x.x:8501 (for access from other devices)

---

## Using the Application

### 1. **Configure Your Trip** (Left Sidebar)

#### Location Details
- **From City**: Your departure city (e.g., "New Delhi")
- **Destination City**: Where you want to travel (e.g., "Paris")

#### Travel Dates
- **Departure Date**: When you're leaving
- **Return Date**: When you're coming back
- The app automatically calculates trip duration

#### Travel Details
- **Number of Travelers**: 1-20 people
- **Travel Style**: Choose from:
  - Budget-Friendly
  - Moderate
  - Luxury
  - Adventure
  - Relaxation
  - Cultural
  - Family-Friendly

#### Budget Planning
- **Budget per Person**: Set in USD
- View automatic total budget calculation

#### Interests & Preferences
- **Your Interests**: Describe what you enjoy (e.g., "sightseeing, food, museums")
- **Dietary Restrictions**: Select any dietary needs
- **Accommodation Type**: Preferred lodging style

### 2. **Generate Your Plan**
- Click the **"🚀 Generate Travel Plan"** button
- Watch the progress bar and status updates
- AI agents will work sequentially:
  1. Location Expert researches logistics
  2. Guide Expert finds attractions
  3. Planning Expert creates itinerary

### 3. **Review Your Itinerary**

The results are organized in **5 tabs**:

#### Tab 1: 📋 Complete Itinerary
- Full travel plan with all details
- Day-by-day breakdown
- Recommendations and tips

#### Tab 2: 🗺️ Quick Overview
- Trip summary
- Your preferences
- Key information at a glance

#### Tab 3: 💾 Export Options
- **Download as TXT**: Plain text format
- **Download as Markdown**: Formatted markdown
- **Download as JSON**: Structured data with all details
- **Export Logs**: Download agent activity logs

#### Tab 4: 📊 Trip Details
- **Budget Breakdown**: Estimated costs by category
  - Accommodation (35%)
  - Food & Dining (25%)
  - Activities (20%)
  - Transportation (15%)
  - Miscellaneous (5%)
- **Daily Budget**: Per-day spending estimate
- **Pre-Travel Checklist**: Interactive checklist

#### Tab 5: 📝 Agent Logs ⭐ NEW!
- **Real-time Activity Tracking**: See what each AI agent is doing
- **Filter Options**:
  - Filter by Agent (System, Location Expert, Guide Expert, Planning Expert)
  - Filter by Status (Info, Warning, Error)
  - Toggle details on/off
- **System Statistics**:
  - Total plans generated
  - Agents run
  - Tasks completed
  - Log entries count
- **Session Information**: Start time and current time
- **Application Logs**: View complete log file

---

## Understanding the Logs

### Log Entry Format
```
[TIMESTAMP] [AGENT_NAME] ACTION - DETAILS
```

### Example Logs
```
[2025-12-03 21:15:30.123] [System] Plan generation started - Route: New Delhi -> Paris
[2025-12-03 21:15:31.456] [Location Expert] Task assigned - Researching travel logistics
[2025-12-03 21:15:32.789] [Guide Expert] Task assigned - Finding attractions and activities
[2025-12-03 21:15:34.012] [Planning Expert] Task assigned - Creating comprehensive itinerary
[2025-12-03 21:16:45.345] [System] Crew execution completed - Execution time: 71.23s
```

### Log Levels
- **🟢 INFO** (Green): Normal operations
- **🟡 WARNING** (Yellow): Potential issues
- **🔴 ERROR** (Red): Failures or exceptions

### What Gets Logged
1. **System Events**:
   - Application startup
   - Plan generation start/end
   - Agent initialization
   - Crew assembly
   - Execution time

2. **Agent Activities**:
   - Task assignments
   - Task creation
   - Research activities
   - Planning operations

3. **Errors & Warnings**:
   - Missing fields
   - Invalid dates
   - Connection issues
   - Execution failures

### Exporting Logs
- **JSON Format**: Structured data for analysis
- **TXT Format**: Human-readable text file
- Both include timestamps, agents, actions, and details

---

## Troubleshooting

### Issue 1: "Cannot connect to Ollama"
**Solution**:
```bash
# Start Ollama server
ollama serve
```

### Issue 2: "Model llama3.2 not found"
**Solution**:
```bash
# Pull the model
ollama pull llama3.2

# Verify installation
ollama list
```

### Issue 3: "Import Error: cannot import name 'guide_expert'"
**Solution**:
- Make sure all files are in the same directory:
  - `app.py`
  - `TravelAgents.py`
  - `TravelTasks.py`
  - `TravelTools.py`
- Restart the Streamlit app

### Issue 4: Slow Plan Generation
**Causes**:
- Large trip duration
- Complex interests
- System resources

**Solutions**:
- Reduce trip duration for testing
- Simplify interests
- Close other applications
- Check Ollama is using GPU (if available)

### Issue 5: Empty or Incomplete Plans
**Solution**:
- Check Ollama is running: `ollama serve`
- Verify model is loaded: `ollama list`
- Check internet connection (for web searches)
- Review logs in the "Agent Logs" tab for errors

### Issue 6: Application Won't Start
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Clear Streamlit cache
streamlit cache clear

# Restart the app
streamlit run app.py
```

---

## Features Summary

### ✨ New Features in Enhanced Version

1. **📝 Comprehensive Logging System**
   - Real-time agent activity tracking
   - System operation monitoring
   - Error and warning capture
   - Execution time tracking

2. **📊 Advanced Analytics**
   - Session statistics
   - Agent performance metrics
   - Task completion tracking
   - Log entry counts

3. **🔍 Log Filtering & Search**
   - Filter by agent
   - Filter by status level
   - Toggle detail visibility
   - Export filtered logs

4. **💾 Enhanced Export Options**
   - Travel plans in TXT, MD, JSON
   - Agent logs in JSON and TXT
   - Complete session data
   - Structured data for analysis

5. **🎨 Premium UI/UX**
   - Glassmorphism design
   - Animated gradients
   - Responsive layout
   - Interactive elements
   - Real-time progress tracking

6. **📈 Session Management**
   - Travel history tracking
   - Statistics persistence
   - Multi-plan support
   - Session information

---

## Tips for Best Results

1. **Be Specific with Interests**: Instead of "sightseeing", try "historical landmarks, art museums, photography spots"

2. **Realistic Budgets**: Set budgets that match your travel style:
   - Budget: $500-1000/person
   - Moderate: $1000-2500/person
   - Luxury: $2500+/person

3. **Optimal Trip Duration**: 5-10 days works best for detailed itineraries

4. **Check Logs**: Use the Agent Logs tab to monitor progress and troubleshoot issues

5. **Export Everything**: Download your plan and logs for offline access

---

## File Structure

```
AI Power Trip Planer Using CrewAI/
│
├── app.py                    # Main application (ENHANCED)
├── my_app_2.py              # Original application
├── TravelAgents.py          # AI agent definitions
├── TravelTasks.py           # Task definitions
├── TravelTools.py           # Custom tools
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── QUICK_START.md          # This file
├── .gitignore              # Git ignore rules
│
├── trip_planner.log        # Application logs (auto-generated)
├── city_report.md          # Generated reports
├── guide_report.md         # Generated reports
└── travel_plan.md          # Generated reports
```

---

## Support & Contact

**Developer**: Ratnesh Singh  
**Role**: Data Scientist  
**GitHub**: [@Ratnesh-181998](https://github.com/Ratnesh-181998)

For issues or questions:
1. Check the logs in the "Agent Logs" tab
2. Review this guide
3. Check the main README.md
4. Open an issue on GitHub

---

## Quick Commands Reference

```bash
# Start Ollama
ollama serve

# Pull LLaMA model
ollama pull llama3.2

# List installed models
ollama list

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Clear Streamlit cache
streamlit cache clear

# View application logs
type trip_planner.log        # Windows
cat trip_planner.log         # Linux/Mac
```

---

**Happy Traveling! ✈️🌍**
