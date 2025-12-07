# 🌍 Agentic AI Trip Planner - Powered by CrewAI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-1.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)

**An intelligent, multi-agent AI travel planning system that creates personalized itineraries with real-time search capabilities**

[Live Demo](https://agentic-ai-trip-planner-crewai.streamlit.app/) • [Documentation](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/wiki) • [Report Bug](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues) • [Request Feature](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [UI Features](#-ui-features--tabs)
- [5-Tier Fallback System](#-5-tier-fallback-system)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Keys Setup](#-api-keys-setup)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**Agentic AI Trip Planner** is a cutting-edge travel planning application that leverages the power of **multi-agent AI systems** to create comprehensive, personalized travel itineraries. Built with **CrewAI**, it employs specialized AI agents that collaborate to research destinations, find the best deals, and craft detailed day-by-day travel plans.
<img width="1249" height="871" alt="Screenshot 2025-12-03 164138" src="https://github.com/user-attachments/assets/e42f9229-c21c-46e7-bcb9-efb8aea2855f" />

### 🌟 What Makes It Special?

- **🤖 Multi-Agent AI System**: Three specialized AI agents work together (Location Expert, Guide Expert, Planner Expert)
- **🔄 5-Tier Fallback System**: Ensures 99.9% uptime with automatic failover across multiple LLM providers
- **🌐 Real-time Web Search**: Live data from the internet for flights, hotels, attractions, and events
- **📱 Beautiful UI**: Modern, responsive interface with glassmorphism design and gradient themes
- **💾 Search History**: Automatic saving and retrieval of all searches with rich card layouts
- **🎯 Interest-Based Planning**: Customizable itineraries based on 24+ travel interests
- **🌍 Global Coverage**: Support for 50+ countries and 500+ cities worldwide
---
## 🌐🎬 Live Demo
🚀 **Try it now:**
- **Streamlit Profile** - https://share.streamlit.io/user/ratnesh-181998
- **Project Demo** - https://agentic-ai-trip-planner-crewai-ykagvec2ng6raotrdaw6sp.streamlit.app/

---

## ✨ Key Features

### 🤖 AI-Powered Trip Planning
- **Intelligent Agents**: Three specialized AI agents collaborate to create comprehensive travel plans
  - **Location Expert**: Researches transportation, accommodation, costs, weather, and visa requirements
  - **Guide Expert**: Discovers attractions, restaurants, activities, and local events
  - **Planner Expert**: Creates detailed day-by-day itineraries with timings and budget breakdowns
<img width="1936" height="1351" alt="Screenshot 2025-12-03 230304" src="https://github.com/user-attachments/assets/f33d508d-79f4-4b2d-9a0e-762e310263c5" />

### 🔍 Comprehensive Search Capabilities
- **✈️ Flight Search**: Real-time flight options with pricing and schedules
- **🏨 Hotel Search**: Accommodation recommendations with ratings and prices
- **🚆 Train Search**: Railway options for intercity and international travel
- **🚌 Bus Search**: Budget-friendly bus routes and schedules

### 🎨 Advanced UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Glassmorphism Effects**: Modern, translucent design elements
- **Gradient Themes**: Beautiful color gradients inspired by nature (sunrise/sunset)
- **Interactive Cards**: Rich destination cards with images and video previews
- **Dark/Light Modes**: Automatic theme adaptation

### 📊 Smart Features
- **Multi-Interest Selection**: Choose from 24+ travel interests
- **Traveler Customization**: Specify adults and children counts
- **Date Range Planning**: Flexible departure and return dates
- **Budget Estimation**: Automatic cost calculations per person
- **History Tracking**: All searches saved with metadata and timestamps

---

## 🛠️ Tech Stack

### **Core Technologies**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Primary programming language |
| **Streamlit** | 1.28+ | Web application framework |
| **CrewAI** | 1.6.1+ | Multi-agent AI orchestration |
| **LangChain** | 0.1.0+ | LLM integration and chaining |

### **AI/LLM Providers**

| Provider | Models | Tier |
|----------|--------|------|
| **Groq** | llama-3.3-70b, llama-3.1-8b, mixtral-8x7b, gemma2-9b | Tier 1-4 |
| **Google Gemini** | gemini-2.0-flash, gemini-1.5-pro | Tier 3-4 |
| **Ollama** | llama3.2 (local) | Tier 5 |

### **Search & Tools**

- **DuckDuckGo Search** (4.0+): Web search without API keys
- **Serper API**: Advanced Google search integration (optional)
- **Browserless API**: Web scraping capabilities (optional)

### **Data & Storage**

- **Python-dotenv**: Environment variable management
- **SQLite3**: Local database for caching
- **File System**: JSON/TXT storage for search history

### **Frontend**

- **HTML5/CSS3**: Custom styling and layouts
- **JavaScript**: Interactive elements (embedded in Streamlit)
- **Base64 Encoding**: Image handling and optimization

---

## 🏗️ Architecture

### Multi-Agent System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INPUT                               │
│  (Destination, Dates, Interests, Travelers)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  CREW ORCHESTRATOR                           │
│              (CrewAI Sequential Process)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   AGENT 1    │ │   AGENT 2    │ │   AGENT 3    │
│  Location    │ │    Guide     │ │   Planner    │
│   Expert     │ │   Expert     │ │   Expert     │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       │ Web Search     │ Web Search     │ Synthesis
       │ Tools          │ Tools          │ Tools
       ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────┐
│              KNOWLEDGE BASE & CONTEXT                         │
│  (Transportation, Hotels, Attractions, Events, Costs)        │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FINAL ITINERARY OUTPUT                          │
│  (Day-by-day plan, Budget, Tips, Recommendations)           │
└─────────────────────────────────────────────────────────────┘
```

### 5-Tier Fallback Architecture

```
Request → Tier 1 (Groq llama-3.3-70b) ──✓──> Success
              │
              ✗ (Rate Limit/Error)
              │
              ▼
          Tier 2 (Groq llama-3.1-8b) ──✓──> Success
              │
              ✗
              ▼
          Tier 3 (Groq mixtral-8x7b) ──✓──> Success
              │
              ✗
              ▼
          Tier 4 (Google Gemini) ──✓──> Success
              │
              ✗
              ▼
          Tier 5 (Ollama Local) ──✓──> Success
```

---

## 🎨 UI Features & Tabs

### 1. 🤖 **AI Trip Planner** (Main Tab)
The core feature where users input their travel details and receive AI-generated itineraries.

**Features:**
- **Smart Location Selection**: Dropdown menus for 50+ countries and 500+ cities
- **Date Range Picker**: Flexible departure and return date selection
- **Traveler Configuration**: Separate inputs for adults and children
- **Interest Multiselect**: 24+ categories including:
  - 🏛️ Sightseeing & Landmarks
  - 🍕 Food & Dining
  - 🎨 Art & Museums
  - 🏖️ Beach & Relaxation
  - ⛰️ Adventure & Hiking
  - 🎭 Culture & History
  - 🛍️ Shopping
  - 🎉 Nightlife & Parties
  - And 16 more...

**Output Includes:**
- Comprehensive city introduction
- Day-by-day detailed itinerary with timings
- Restaurant recommendations with cuisine types
- Budget breakdown (flights, hotels, food, activities)
- Visa requirements and travel tips
- Weather forecast and packing suggestions
<img width="940" height="510" alt="image" src="https://github.com/user-attachments/assets/481abb62-1191-43c2-8742-67ceea9dbcca" />
<img width="940" height="504" alt="image" src="https://github.com/user-attachments/assets/cba55e88-e3f0-41d6-80f5-86b4fcca1fd3" />
<img width="940" height="504" alt="image" src="https://github.com/user-attachments/assets/b065db55-f1d0-4f87-997a-a7889b42ffa2" />
<img width="940" height="519" alt="image" src="https://github.com/user-attachments/assets/fc76bc13-3bee-4c21-acbe-dfe0b017591c" />
<img width="940" height="500" alt="image" src="https://github.com/user-attachments/assets/687b3758-13f3-45fb-9444-bbccc83f6b9e" />
<img width="940" height="501" alt="image" src="https://github.com/user-attachments/assets/fa819cff-5e76-40ce-9251-ed3cda9cd967" />
<img width="940" height="892" alt="image" src="https://github.com/user-attachments/assets/836e84eb-37fc-4522-82f3-dc2f0351550d" />
<img width="940" height="793" alt="image" src="https://github.com/user-attachments/assets/327645ab-5f68-4de0-bc99-cfa596191225" />
<img width="940" height="874" alt="image" src="https://github.com/user-attachments/assets/fabf64ca-03bc-4062-a7a4-cd100243bffe" />
<img width="940" height="874" alt="image" src="https://github.com/user-attachments/assets/046ef288-e347-4e1c-9f39-51d043d6e93a" />
<img width="940" height="497" alt="image" src="https://github.com/user-attachments/assets/03003716-091c-4f57-8bf1-8bf6d7e3f1b1" />
<img width="940" height="486" alt="image" src="https://github.com/user-attachments/assets/0bb33bb8-af8f-464d-9299-be1dd7e76c0c" />
<img width="940" height="493" alt="image" src="https://github.com/user-attachments/assets/d23e9bf0-7141-494e-ba09-d394cf4e15c0" />

### 2. 📜 **AI Trip Planner History**
View and manage all previously generated trip plans.

**Features:**
- **Rich Card Layout**: Beautiful gradient cards showing trip summaries
- **Metadata Display**: Destination, dates, creation timestamp, file size
- **Content Preview**: Expandable sections to view full itinerary
- **Download Options**: Export any plan as TXT file
- **Smart Sorting**: Newest plans first
- **Search Filters**: (Coming soon)
<img width="940" height="508" alt="image" src="https://github.com/user-attachments/assets/bf583f98-a122-4c4d-a7f7-7c71be57b63a" />

### 3. 🎯 **Explore by Interest**
Discover destinations based on specific travel interests.

**17 Interest Categories:**
1. 🏖️ Beach Destinations
2. ⛰️ Mountain & Adventure
3. 🏛️ Historical Sites
4. 🍕 Food & Culinary Tours
5. 🎨 Art & Culture
6. 🏙️ Urban Exploration
7. 🌳 Nature & Wildlife
8. 🏰 Castles & Palaces
9. 🎭 Festivals & Events
10. 🛍️ Shopping Havens
11. 🎉 Nightlife Hotspots
12. 📸 Photography Spots
13. 🧘 Wellness & Spa
14. 🏃 Sports & Fitness
15. 👨‍👩‍👧 Family-Friendly
16. 💑 Romantic Getaways
17. 🎓 Educational Tours

**Each Category Shows:**
- Curated destination cards with images
- Price ranges (flights + hotels)
- Best time to visit
- Top attractions
- Insider tips

### 4. ✈️ **Flights Search**
AI-powered flight search with real-time data.

**Features:**
- **Route Input**: From/To city selection
- **Date Selection**: Departure and return dates
- **Passenger Details**: Adults and children counts
- **Class Selection**: Economy, Business, First Class
- **AI Analysis**: Best deals, layover optimization, price trends
- **Results Include**:
  - Multiple airline options
  - Price comparisons
  - Flight duration and layovers
  - Booking links
  - Price alerts and recommendations

### 5. 📜 **Flight History**
Track all flight searches with detailed metadata.

### 6. 🏨 **Hotels Search**
Comprehensive hotel search powered by AI.

**Features:**
- **Location-Based**: City/area selection
- **Check-in/Check-out Dates**: Flexible date ranges
- **Guest Configuration**: Rooms, adults, children
- **Amenity Filters**: WiFi, Pool, Gym, Breakfast, etc.
- **AI Recommendations**:
  - Best value hotels
  - Luxury options
  - Budget-friendly choices
  - Location-based suggestions
  - User ratings and reviews

### 7. 📜 **Hotel History**
Archive of all hotel searches with rich previews.

### 8. 🚆 **Trains Search**
Railway options for intercity and international travel.

**Features:**
- **Route Planning**: Origin and destination stations
- **Schedule Search**: Date and time preferences
- **Class Selection**: Sleeper, AC, First Class, etc.
- **AI Insights**:
  - Fastest routes
  - Most scenic journeys
  - Budget options
  - Booking tips

### 9. 📜 **Train History**
Historical train search records.

### 10. 🚌 **Buses Search**
Budget-friendly bus travel options.

**Features:**
- **Route Search**: City-to-city bus services
- **Operator Comparison**: Multiple bus companies
- **Amenity Filters**: AC, WiFi, Sleeper, etc.
- **AI Recommendations**: Best operators, timing, pricing

### 11. 📜 **Bus History**
Archive of bus search results.

### 12. 🌟 **Destinations**
Curated list of popular destinations worldwide.

**Features:**
- **Destination Cards**: Beautiful cards with images/videos
- **Quick Info**: Country, description, price range, hotel options
- **5-Second Video Previews**: Autoplay destination highlights
- **Interactive Filters**: By region, budget, season
- **Featured Destinations**:
  - Bora Bora, French Polynesia
  - Monaco, France
  - Jerusalem, Israel
  - Bologna, Italy
  - And many more...

### 13. 💡 **Travel Tips**
Expert advice and travel hacks.

**Categories:**
- **Pre-Trip Planning**: Visa, insurance, packing
- **During Travel**: Safety, communication, local customs
- **Budget Tips**: Money-saving strategies
- **Health & Safety**: Medical prep, emergency contacts
- **Cultural Etiquette**: Do's and don'ts by country
- **Tech Tips**: Apps, tools, connectivity

---

## 🔄 5-Tier Fallback System

Our revolutionary **5-Tier Fallback System** ensures **99.9% uptime** by automatically switching between LLM providers when issues occur.

### How It Works

| Tier | Provider | Model | Speed | Quality | Fallback Trigger |
|------|----------|-------|-------|---------|------------------|
| **1** | Groq | llama-3.3-70b-versatile | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Rate limit, API error |
| **2** | Groq | llama-3.1-8b-instant | ⚡⚡⚡ | ⭐⭐⭐⭐ | Rate limit, API error |
| **3** | Groq | mixtral-8x7b-32768 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Rate limit, API error |
| **4** | Google | gemini-2.0-flash | ⚡⚡ | ⭐⭐⭐⭐ | Network error, auth failure |
| **5** | Ollama | llama3.2 (local) | ⚡ | ⭐⭐⭐ | All cloud providers fail |

### Benefits

- **Zero Downtime**: Automatic failover in milliseconds
- **Cost Optimization**: Uses free tiers first, paid tiers as backup
- **Offline Capability**: Tier 5 works without internet
- **User Transparency**: Real-time status updates during fallback
- **Smart Recovery**: Automatically returns to Tier 1 when available

### Visual Alerts

The system provides high-visibility alerts during fallback:
- 🚨 **Red Alert**: Tier 1 failure, switching to Tier 2-3
- ⚠️ **Orange Alert**: Cloud providers failed, switching to Tier 5
- ✅ **Green Success**: Operation completed successfully

---

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Git** (for cloning repository)
- **Ollama** (optional, for Tier 5 local LLM)

### Step 1: Clone Repository

```bash
git clone https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI.git
cd Agentic-AI-Trip-Planner-CrewAI
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your API keys (see [API Keys Setup](#-api-keys-setup))

### Step 5: Run the Application

```bash
streamlit run ratnesh_app_ULTIMATE.py
```

The app will open in your browser at `http://localhost:8501`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required for Tier 1-3 (Groq)
GROQ_API_KEY=your_groq_api_key_here

# Required for Tier 4 (Google Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# Optional - Advanced Search (if using Serper)
SERPER_API_KEY=your_serper_api_key_here

# Optional - Web Scraping (if using Browserless)
BROWSERLESS_API_KEY=your_browserless_api_key_here

# Optional - Ollama Configuration (Tier 5)
OLLAMA_HOST=http://localhost:11434
```

### LLM Provider Selection

In the sidebar, you can choose:
- **Auto (5-Tier Fallback)**: Recommended - uses all tiers
- **Groq Only**: Fast, requires API key
- **Google Only**: Uses Gemini models
- **Ollama Only**: Offline mode, requires local Ollama

---

## 🔑 API Keys Setup

### 1. Groq API Key (Free)

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into `.env` file

**Free Tier**: 30 requests/minute, 14,400 requests/day

### 2. Google Gemini API Key (Free)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

**Free Tier**: 60 requests/minute

### 3. Serper API Key (Optional)

1. Visit [Serper.dev](https://serper.dev/)
2. Sign up for free account
3. Get API key from dashboard
4. Copy and paste into `.env` file

**Free Tier**: 2,500 searches/month

### 4. Ollama Setup (Optional - Tier 5)

For offline capability:

```bash
# Install Ollama
# Visit https://ollama.ai/ and download for your OS

# Pull the model
ollama pull llama3.2

# Verify it's running
ollama list
```

---

## 📖 Usage

### Basic Trip Planning

1. **Open the App**: Navigate to `http://localhost:8501`
2. **Select Locations**: Choose from/to country and city
3. **Set Dates**: Pick departure and return dates
4. **Configure Travelers**: Enter number of adults and children
5. **Choose Interests**: Select from 24+ travel interests
6. **Generate Plan**: Click "🚀 Generate Travel Plan"
7. **Review Output**: Get detailed day-by-day itinerary
8. **Save/Download**: Plans auto-save to `trip_plans/` folder

### Flight/Hotel/Train/Bus Search

1. Navigate to respective tab
2. Enter route details (from/to)
3. Select dates and passenger count
4. Click search button
5. Review AI-generated options
6. Download results or view in history

### Explore by Interest

1. Go to "🎯 Explore by Interest" tab
2. Browse 17 interest categories
3. Click on any category to see curated destinations
4. View destination cards with images, prices, and details

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Configure Git LFS** (for large files):
```bash
git lfs install
git lfs track "*.png" "*.jpg" "*.mp4"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

3. **Deploy on Streamlit**:
   - Visit [Streamlit Cloud](https://streamlit.io/cloud)
   - Connect your GitHub repository
   - Select `ratnesh_app_ULTIMATE.py` as main file
   - Add environment variables (API keys)
   - Click "Deploy"

### Environment Variables on Streamlit Cloud

In Streamlit Cloud settings, add:
```
GROQ_API_KEY=your_key
GOOGLE_API_KEY=your_key
SERPER_API_KEY=your_key (optional)
```

---

## 📁 Project Structure

```
Agentic-AI-Trip-Planner-CrewAI/
│
├── ratnesh_app_ULTIMATE.py      # Main Streamlit application
├── TravelAgents.py               # AI agent definitions
├── TravelTasks.py                # Task definitions for agents
├── TravelTasks_LEGACY.py         # Legacy detailed tasks
├── TravelTools.py                # Search and web tools
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
├── .gitattributes                # Git LFS configuration
│
├── images/                       # Destination images
│   ├── bologna.png
│   ├── borabora.png
│   ├── jerusalem.png
│   └── monaco.png
│
├── trip_plans/                   # Saved trip itineraries
├── Flight_Search_History/        # Flight search archives
├── Hotel_Search_History/         # Hotel search archives
├── Train_Search_History/         # Train search archives
├── Bus_Search_History/           # Bus search archives
│
├── docs/                         # Documentation files
│   ├── 5_TIER_SYSTEM.md
│   ├── DEPLOYMENT.md
│   ├── QUICK_START.md
│   └── API_SETUP.md
│
└── README.md                     # This file
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs

1. Check [existing issues](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues)
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version)

### Suggesting Features

1. Open a [feature request](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues/new)
2. Describe the feature and its benefits
3. Provide use cases and examples

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Write unit tests for new features
- Update documentation
- Test on multiple Python versions (3.10, 3.11, 3.12)

---

## 📄 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024 Ratnesh Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Third-Party Licenses

This project uses the following open-source libraries:
- **Streamlit** - Apache License 2.0
- **CrewAI** - MIT License
- **LangChain** - MIT License
- **Groq SDK** - Apache License 2.0
- **Google Generative AI** - Apache License 2.0

---

## 📞 Contact

**RATNESH SINGH**  
*Data Scientist | AI/ML Engineer | 4+ Years Experience*

- 📧 **Email**: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)
- 💼 **LinkedIn**: [linkedin.com/in/ratneshkumar1998](https://www.linkedin.com/in/ratneshkumar1998/)
- 🐙 **GitHub**: [github.com/Ratnesh-181998](https://github.com/Ratnesh-181998)
- 📱 **Phone**: +91-947XXXXX46

### Project Links

- 🌐 **Live Demo**: [Streamlit App](https://agentic-ai-trip-planner-crewai-ykagvec2ng6raotrdaw6sp.streamlit.app/)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/wiki)
- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI/discussions)

---

## 🙏 Acknowledgments

Special thanks to:
- **CrewAI Team** - For the amazing multi-agent framework
- **Streamlit** - For the intuitive web app framework
- **Groq** - For lightning-fast LLM inference
- **Google** - For Gemini AI models
- **Ollama** - For local LLM capabilities
- **Open Source Community** - For continuous inspiration and support

---

## 📊 Stats & Metrics

![GitHub Stars](https://img.shields.io/github/stars/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI?style=social)
![GitHub Issues](https://img.shields.io/github/issues/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Ratnesh-181998/Agentic-AI-Trip-Planner-CrewAI)

---

## 🗺️ Roadmap

### Version 2.0 (Upcoming)

- [ ] **Real-time Booking Integration**: Direct booking for flights, hotels, trains
- [ ] **Multi-language Support**: 10+ languages
- [ ] **Mobile App**: React Native version
- [ ] **Social Features**: Share itineraries, collaborate with friends
- [ ] **AI Chat Assistant**: Conversational interface for planning
- [ ] **Price Alerts**: Notifications for price drops
- [ ] **Offline Mode**: Full functionality without internet
- [ ] **Advanced Analytics**: Travel insights and statistics

### Version 1.5 (In Progress)

- [x] 5-Tier Fallback System
- [x] Interest-based exploration
- [x] Search history with rich cards
- [ ] User authentication
- [ ] Saved favorites
- [ ] Export to PDF/Google Calendar

---

<div align="center">

**Made with ❤️ by Ratnesh Singh**

⭐ **Star this repo if you find it helpful!** ⭐

[⬆ Back to Top](#-agentic-ai-trip-planner---powered-by-crewai)

</div>
