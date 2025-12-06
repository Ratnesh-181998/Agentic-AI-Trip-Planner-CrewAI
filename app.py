from TravelAgents import guide_expert, location_expert, planner_expert
from TravelTasks import location_task, guide_task, planner_task
from crewai import Crew, Process
import streamlit as st
from datetime import datetime, timedelta
import json
import time
import logging
import sys
import os
import shutil
from io import StringIO
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trip_planner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Custom log handler to capture logs in session state
class StreamlitLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []
    
    def emit(self, record):
        log_entry = self.format(record)
        self.logs.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'level': record.levelname,
            'message': log_entry
        })

# Initialize log handler
if 'log_handler' not in st.session_state:
    st.session_state.log_handler = StreamlitLogHandler()
    st.session_state.log_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(st.session_state.log_handler)

# Page Configuration
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger.info("Application started")

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Poppins:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Force dark text for markdown elements */
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown span {
        color: #2d2d2d !important;
    }
    
    /* Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #2d2d2d;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.3);
    }
    
    .main-header p {
        color: #2d2d2d;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: black;
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stDateInput input, .stNumberInput input, .stSelectbox select {
        background: #2d2d2d !important;
        color: white !important;
        border: 2px solid #555555 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.02);
        background: #3d3d3d !important;
    }

    /* Input Labels */
    .stTextInput label, .stTextArea label, .stDateInput label, .stNumberInput label, .stSelectbox label, .stMultiSelect label {
        color: black !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #2d2d2d !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #000000 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: black;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: black !important;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateX(10px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: black;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: rgba(0, 0, 0, 0.9);
        font-size: 0.95rem;
    }
    
    /* Log Container */
    .log-container {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 12px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
        color: #00ff00;
    }
    
    .log-entry {
        margin: 0.25rem 0;
        padding: 0.25rem;
        border-left: 3px solid #667eea;
        padding-left: 0.5rem;
    }
    
    .log-info { color: #00ff00; }
    .log-warning { color: #ffaa00; }
    .log-error { color: #ff0000; }
    .log-debug { color: #00aaff; }
    
    /* Animation for loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-text {
        animation: pulse 2s ease-in-out infinite;
        font-size: 1.2rem;
        color: white;
        text-align: center;
        padding: 2rem;
    }
    
    /* Credit */
    .credit {
        text-align: center;
        color: #000000;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        font-weight: 600;
    }
    
    .credit a {
        color: #000080;
        text-decoration: none;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'travel_history' not in st.session_state:
    st.session_state.travel_history = []
    logger.info("Initialized travel history")

if 'current_plan' not in st.session_state:
    st.session_state.current_plan = None

if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False

if 'agent_logs' not in st.session_state:
    st.session_state.agent_logs = []

if 'system_stats' not in st.session_state:
    st.session_state.system_stats = {
        'total_plans': 0,
        'total_agents_run': 0,
        'total_tasks_completed': 0,
        'session_start': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Header
st.markdown("""
<div class="main-header">
    <h1>✈️ AI-Powered Trip Planner</h1>
    <p>Your Intelligent Travel Companion - Plan Perfect Trips with AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - User Inputs
with st.sidebar:
    st.markdown("### 🎯 Trip Configuration")
    st.markdown("---")
    
    # Basic Information
    st.markdown("#### 📍 Location Details")
    
    # Predefined Cities Database
    LOCATIONS = {
        "India": ["New Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur", "Goa", "Ahmedabad"],
        "USA": ["New York", "Los Angeles", "San Francisco", "Chicago", "Miami", "Las Vegas", "Washington DC", "Boston"],
        "France": ["Paris", "Nice", "Lyon", "Bordeaux", "Marseille", "Strasbourg"],
        "United Kingdom": ["London", "Manchester", "Edinburgh", "Liverpool", "Birmingham"],
        "Italy": ["Rome", "Venice", "Florence", "Milan", "Naples", "Amalfi Coast"],
        "Japan": ["Tokyo", "Kyoto", "Osaka", "Hiroshima", "Sapporo"],
        "UAE": ["Dubai", "Abu Dhabi", "Sharjah"],
        "Thailand": ["Bangkok", "Phuket", "Chiang Mai", "Krabi"],
        "Singapore": ["Singapore"],
        "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Gold Coast"],
        "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
        "Switzerland": ["Zurich", "Geneva", "Interlaken", "Lucerne"],
        "Spain": ["Barcelona", "Madrid", "Seville", "Valencia"],
        "Canada": ["Toronto", "Vancouver", "Montreal", "Ottawa"],
        "Other": ["Type Manually"]
    }
    
    # From Location
    st.markdown("**🏡 From**")
    col_from_1, col_from_2 = st.columns(2)
    with col_from_1:
        from_country = st.selectbox("Country", list(LOCATIONS.keys()), index=0, key="from_country")
    with col_from_2:
        if from_country == "Other":
            from_city = st.text_input("City", value="New Delhi", key="from_city_manual")
        else:
            from_city = st.selectbox("City", LOCATIONS[from_country], key="from_city_select")
            
    # Destination Location
    st.markdown("**✈️ Destination**")
    col_dest_1, col_dest_2 = st.columns(2)
    with col_dest_1:
        dest_country = st.selectbox("Country", list(LOCATIONS.keys()), index=2, key="dest_country") # Default to France
    with col_dest_2:
        if dest_country == "Other":
            destination_city = st.text_input("City", value="Paris", key="dest_city_manual")
        else:
            destination_city = st.selectbox("City", LOCATIONS[dest_country], key="dest_city_select")
    
    st.markdown("#### 📅 Travel Dates")
    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input("Departure", value=datetime.now() + timedelta(days=30))
    with col2:
        date_to = st.date_input("Return", value=datetime.now() + timedelta(days=37))
    
    # Calculate trip duration
    if date_to > date_from:
        trip_duration = (date_to - date_from).days
        st.info(f"📊 Trip Duration: **{trip_duration} days**")
    else:
        st.error("⚠️ Return date must be after departure date")
        trip_duration = 0
    
    st.markdown("#### 👥 Travel Details")
    num_travelers = st.number_input("Number of Travelers", min_value=1, max_value=20, value=2)
    
    travel_style = st.selectbox(
        "🎨 Travel Style",
        ["Budget-Friendly", "Moderate", "Luxury", "Adventure", "Relaxation", "Cultural", "Family-Friendly"]
    )
    
    st.markdown("#### 💰 Budget Planning")
    budget_per_person = st.number_input(
        "Budget per Person (USD)",
        min_value=100,
        max_value=50000,
        value=1500,
        step=100,
        help="Approximate budget per person in USD"
    )
    
    total_budget = budget_per_person * num_travelers
    st.success(f"💵 Total Budget: **${total_budget:,}**")
    
    st.markdown("#### 🎯 Interests & Preferences")
    interests = st.text_area(
        "Your Interests",
        value="sightseeing, local cuisine, photography, museums",
        help="What activities do you enjoy? (e.g., food, adventure, culture, shopping)",
        height=100
    )
    
    dietary_restrictions = st.multiselect(
        "🍽️ Dietary Restrictions",
        ["None", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-Free", "Lactose-Free"]
    )
    
    accommodation_type = st.selectbox(
        "🏨 Preferred Accommodation",
        ["Hotels", "Hostels", "Airbnb", "Resorts", "Boutique Hotels", "Mix"]
    )
    
    st.markdown("---")
    
    # Generate Button
    generate_button = st.button("🚀 Generate Travel Plan", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    st.metric("Plans Generated", st.session_state.system_stats['total_plans'])
    st.metric("Agents Run", st.session_state.system_stats['total_agents_run'])
    st.metric("Tasks Completed", st.session_state.system_stats['total_tasks_completed'])
    
    st.markdown("---")
    st.markdown("### 📂 Saved Trips History")
    
    if not os.path.exists("trip_plans"):
        os.makedirs("trip_plans")
        
    saved_trips = sorted([d for d in os.listdir("trip_plans") if os.path.isdir(os.path.join("trip_plans", d))], reverse=True)
    
    if saved_trips:
        selected_trip = st.selectbox("Select a past trip", ["Select..."] + saved_trips)
        if selected_trip != "Select...":
            st.success(f"📂 Found in: trip_plans/{selected_trip}")
    else:
        st.info("No saved trips yet.")

# Function to add agent log
def add_agent_log(agent_name, action, status="info", details=""):
    log_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        'agent': agent_name,
        'action': action,
        'status': status,
        'details': details
    }
    st.session_state.agent_logs.append(log_entry)
    
    # Also log to file
    if status == "error":
        logger.error(f"[{agent_name}] {action} - {details}")
    elif status == "warning":
        logger.warning(f"[{agent_name}] {action} - {details}")
    else:
        logger.info(f"[{agent_name}] {action} - {details}")

# Main Content Area
if not generate_button and not st.session_state.plan_generated:
    # Welcome Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI-Powered</div>
            <div class="feature-desc">Advanced AI agents work together to create your perfect itinerary</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Personalized</div>
            <div class="feature-desc">Tailored recommendations based on your interests and preferences</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Comprehensive</div>
            <div class="feature-desc">Complete travel info including visa, weather, budget, and activities</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How It Works
    with st.expander("📖 How It Works", expanded=True):
        st.markdown("""
        ### 🔄 Our AI Travel Planning Process
        
        1. **🔍 Location Expert** - Researches travel logistics, visa requirements, weather, and local events
        2. **🗺️ Guide Expert** - Finds the best attractions, restaurants, and activities based on your interests
        3. **📋 Planning Expert** - Combines all information into a detailed, day-by-day itinerary
        
        #### ✨ What You'll Get:
        - 📍 Detailed city introduction and overview
        - 🗓️ Day-by-day itinerary with time allocations
        - 🍽️ Restaurant and food recommendations
        - 🏨 Accommodation suggestions
        - 💰 Budget breakdown and cost estimates
        - 🚆 Transportation options and tips
        - 📋 Visa and travel document requirements
        - 🌤️ Weather information and packing tips
        - 🎉 Local events and festivals
        - 💡 Insider tips and recommendations
        """)
    
    # Sample Destinations
    with st.expander("🌍 Popular Destinations"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**🇫🇷 Paris**\nRomance & Culture")
        with col2:
            st.markdown("**🇯🇵 Tokyo**\nTech & Tradition")
        with col3:
            st.markdown("**🇮🇹 Rome**\nHistory & Cuisine")
        with col4:
            st.markdown("**🇹🇭 Bangkok**\nAdventure & Food")

# Generate Travel Plan
if generate_button:
    # Validation
    if not from_city or not destination_city or not interests:
        st.error("⚠️ Please fill in all required fields (From City, Destination, Interests)")
        logger.warning("Plan generation attempted with missing fields")
    elif trip_duration <= 0:
        st.error("⚠️ Please select valid travel dates (Return date must be after departure date)")
        logger.warning("Plan generation attempted with invalid dates")
    else:
        st.session_state.plan_generated = True
        st.session_state.agent_logs = []  # Clear previous logs
        
        logger.info(f"Starting travel plan generation: {from_city} -> {destination_city}")
        add_agent_log("System", "Plan generation started", "info", f"Route: {from_city} -> {destination_city}")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        log_display = st.empty()
        
        try:
            # Step 1: Initialize
            status_text.markdown('<div class="loading-text">🔧 Initializing AI Travel Agents...</div>', unsafe_allow_html=True)
            progress_bar.progress(10)
            add_agent_log("System", "Initializing AI agents", "info", "Loading CrewAI framework")
            time.sleep(0.5)
            
            # Import agents (lazy import to avoid startup errors)
            add_agent_log("System", "Importing agent modules", "info")
            from TravelAgents import guide_expert, location_expert, planner_expert
            from TravelTasks import location_task, guide_task, planner_task
            from crewai import Crew, Process
            
            add_agent_log("System", "Agents imported successfully", "info", "3 agents loaded")
            st.session_state.system_stats['total_agents_run'] += 3
            
            # Step 2: Location Research
            status_text.markdown('<div class="loading-text">🔍 Researching travel logistics and requirements...</div>', unsafe_allow_html=True)
            progress_bar.progress(25)
            add_agent_log("Location Expert", "Task assigned", "info", "Researching travel logistics")
            loc_task = location_task(location_expert, from_city, destination_city, date_from, date_to)
            add_agent_log("Location Expert", "Task created", "info", f"Analyzing route: {from_city} -> {destination_city}")
            
            # Step 3: Guide Research
            status_text.markdown('<div class="loading-text">🗺️ Finding best attractions and activities...</div>', unsafe_allow_html=True)
            progress_bar.progress(40)
            add_agent_log("Guide Expert", "Task assigned", "info", "Finding attractions and activities")
            guid_task = guide_task(guide_expert, destination_city, interests, date_from, date_to)
            add_agent_log("Guide Expert", "Task created", "info", f"Interests: {interests}")
            
            # Step 4: Planning
            status_text.markdown('<div class="loading-text">📋 Creating your personalized itinerary...</div>', unsafe_allow_html=True)
            progress_bar.progress(55)
            add_agent_log("Planning Expert", "Task assigned", "info", "Creating comprehensive itinerary")
            plan_task = planner_task([loc_task, guid_task], planner_expert, destination_city, interests, date_from, date_to)
            add_agent_log("Planning Expert", "Task created", "info", f"Duration: {trip_duration} days")
            st.session_state.system_stats['total_tasks_completed'] += 3
            
            # Step 5: Crew Assembly
            status_text.markdown('<div class="loading-text">🤝 Assembling AI crew...</div>', unsafe_allow_html=True)
            progress_bar.progress(70)
            add_agent_log("System", "Assembling crew", "info", "Coordinating 3 agents")
            
            crew = Crew(
                agents=[location_expert, guide_expert, planner_expert],
                tasks=[loc_task, guid_task, plan_task],
                process=Process.sequential,
                full_output=True,
                verbose=True,
            )
            add_agent_log("System", "Crew assembled", "info", "Sequential processing mode")
            
            # Step 6: Execute
            status_text.markdown('<div class="loading-text">⚡ Generating your travel plan... This may take a few minutes...</div>', unsafe_allow_html=True)
            progress_bar.progress(85)
            add_agent_log("System", "Crew execution started", "info", "AI agents working...")
            
            # Capture crew output
            start_time = time.time()
            result = crew.kickoff()
            execution_time = time.time() - start_time
            
            add_agent_log("System", "Crew execution completed", "info", f"Execution time: {execution_time:.2f}s")
            
            # Save all outputs to a unique folder
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            safe_dest = "".join([c for c in destination_city if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
            folder_name = f"trip_plans/{timestamp}_{safe_dest}"
            
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                
            # Copy generated files
            files_to_save = ['city_report.md', 'guide_report.md', 'travel_plan.md']
            for file in files_to_save:
                if os.path.exists(file):
                    shutil.copy(file, f"{folder_name}/{file}")
            
            # Save logs
            with open(f"{folder_name}/agent_logs.json", 'w') as f:
                json.dump(st.session_state.agent_logs, f, indent=2)
                
            add_agent_log("System", "Outputs saved", "info", f"Saved to {folder_name}")
            
            # Step 7: Finalize
            status_text.markdown('<div class="loading-text">✨ Finalizing your itinerary...</div>', unsafe_allow_html=True)
            progress_bar.progress(100)
            add_agent_log("System", "Finalizing results", "info", "Processing output")
            time.sleep(0.5)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Store result
            st.session_state.current_plan = str(result)
            add_agent_log("System", "Plan saved", "info", f"Plan length: {len(str(result))} characters")
            
            # Add to history
            st.session_state.travel_history.append({
                'destination': destination_city,
                'from': from_city,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'duration': trip_duration,
                'travelers': num_travelers,
                'budget': total_budget
            })
            
            st.session_state.system_stats['total_plans'] += 1
            add_agent_log("System", "Plan generation completed", "info", f"Total plans: {st.session_state.system_stats['total_plans']}")
            
            st.success("✅ Your personalized travel plan is ready!")
            logger.info(f"Plan generation successful in {execution_time:.2f}s")
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            st.error(f"❌ An error occurred while generating your travel plan: {error_msg}")
            add_agent_log("System", "Error occurred", "error", error_msg)
            logger.error(f"Plan generation failed: {error_msg}\n{error_trace}")
            
            with st.expander("🔍 Error Details"):
                st.code(error_trace)
            
            st.info("💡 Tip: Make sure Ollama is running locally with the llama3.2 model installed.")
            st.session_state.plan_generated = False

# Display Results
if st.session_state.plan_generated and st.session_state.current_plan:
    st.markdown("---")
    st.markdown("## ✅ Your AI-Generated Travel Plan")
    
    # Trip Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Destination", destination_city)
    with col2:
        st.metric("📅 Duration", f"{trip_duration} days")
    with col3:
        st.metric("👥 Travelers", num_travelers)
    with col4:
        st.metric("💰 Budget", f"${total_budget:,}")
    
    st.markdown("---")
    
    # Tabbed Interface for Results
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Complete Itinerary", "🔍 Location Expert", "🗺️ Guide Expert", "💾 Export Options", "📊 Trip Details", "📝 Agent Logs"])
    
    with tab1:
        st.markdown("### 📋 Your Complete Travel Itinerary")
        st.markdown(st.session_state.current_plan)
        
    with tab2:
        st.markdown("### 🔍 Location Expert Report")
        st.info("This report covers travel logistics, visa requirements, weather, and costs.")
        try:
            with open('city_report.md', 'r', encoding='utf-8') as f:
                location_report = f.read()
            st.markdown(location_report)
        except FileNotFoundError:
            st.warning("Location report not found. Please generate a plan first.")
            
    with tab3:
        st.markdown("### 🗺️ Guide Expert Report")
        st.info("This report covers attractions, food recommendations, and activities.")
        try:
            with open('guide_report.md', 'r', encoding='utf-8') as f:
                guide_report = f.read()
            st.markdown(guide_report)
        except FileNotFoundError:
            st.warning("Guide report not found. Please generate a plan first.")
    
    with tab4:
        st.markdown("### 💾 Export Your Travel Plan")
        
        travel_plan_text = st.session_state.current_plan
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Text Export
            st.download_button(
                label="📄 Download as TXT",
                data=travel_plan_text,
                file_name=f"Travel_Plan_{destination_city}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Markdown Export
            st.download_button(
                label="📝 Download as Markdown",
                data=travel_plan_text,
                file_name=f"Travel_Plan_{destination_city}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col3:
            # JSON Export
            plan_data = {
                "destination": destination_city,
                "from_city": from_city,
                "departure_date": date_from.strftime("%Y-%m-%d"),
                "return_date": date_to.strftime("%Y-%m-%d"),
                "duration_days": trip_duration,
                "travelers": num_travelers,
                "travel_style": travel_style,
                "budget_total": total_budget,
                "budget_per_person": budget_per_person,
                "interests": interests,
                "dietary_restrictions": dietary_restrictions,
                "accommodation_type": accommodation_type,
                "itinerary": travel_plan_text,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "agent_logs": st.session_state.agent_logs
            }
            
            st.download_button(
                label="📊 Download as JSON",
                data=json.dumps(plan_data, indent=2),
                file_name=f"Travel_Plan_{destination_city}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Export Logs
        st.markdown("### 📋 Export Logs")
        col1, col2 = st.columns(2)
        
        with col1:
            # Export agent logs as JSON
            logs_json = json.dumps(st.session_state.agent_logs, indent=2)
            st.download_button(
                label="📊 Download Agent Logs (JSON)",
                data=logs_json,
                file_name=f"Agent_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Export agent logs as text
            logs_text = "\n".join([
                f"[{log['timestamp']}] [{log['agent']}] {log['action']} - {log['details']}"
                for log in st.session_state.agent_logs
            ])
            st.download_button(
                label="📄 Download Agent Logs (TXT)",
                data=logs_text,
                file_name=f"Agent_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.info("💡 **Tip:** Save your travel plan in multiple formats for easy access during your trip!")
    
    with tab5:
        st.markdown("### 📊 Detailed Trip Information")
        
        # Budget Breakdown
        st.markdown("#### 💰 Budget Breakdown (Estimated)")
        
        # Rough estimates
        accommodation_pct = 0.35
        food_pct = 0.25
        activities_pct = 0.20
        transport_pct = 0.15
        misc_pct = 0.05
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🏨 Accommodation", f"${int(total_budget * accommodation_pct):,}")
            st.metric("🍽️ Food & Dining", f"${int(total_budget * food_pct):,}")
        
        with col2:
            st.metric("🎡 Activities", f"${int(total_budget * activities_pct):,}")
            st.metric("🚆 Transportation", f"${int(total_budget * transport_pct):,}")
        
        with col3:
            st.metric("🛍️ Miscellaneous", f"${int(total_budget * misc_pct):,}")
            st.metric("📊 Daily Budget", f"${int(total_budget / trip_duration):,}")
        
        st.markdown("---")
        
        # Travel Checklist
        st.markdown("#### ✅ Pre-Travel Checklist")
        
        checklist_items = [
            "Check passport validity (6+ months)",
            "Research visa requirements",
            "Book flights and accommodation",
            "Arrange travel insurance",
            "Notify bank of travel plans",
            "Check vaccination requirements",
            "Download offline maps",
            "Make copies of important documents",
            "Pack according to weather forecast",
            "Exchange currency or arrange payment methods"
        ]
        
        for item in checklist_items:
            st.checkbox(item, key=f"checklist_{item}")
    
    with tab6:
        st.markdown("### 📝 Agent Activity Logs")
        st.markdown("Real-time tracking of all AI agent activities and system operations")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_agent = st.selectbox("Filter by Agent", ["All"] + list(set([log['agent'] for log in st.session_state.agent_logs])))
        with col2:
            filter_status = st.selectbox("Filter by Status", ["All", "info", "warning", "error"])
        with col3:
            show_details = st.checkbox("Show Details", value=True)
        
        # Filter logs
        filtered_logs = st.session_state.agent_logs
        if filter_agent != "All":
            filtered_logs = [log for log in filtered_logs if log['agent'] == filter_agent]
        if filter_status != "All":
            filtered_logs = [log for log in filtered_logs if log['status'] == filter_status]
        
        st.markdown("---")
        
        # Display logs
        if filtered_logs:
            log_html = '<div class="log-container">'
            for log in filtered_logs:
                status_class = f"log-{log['status']}"
                details_str = f" - {log['details']}" if show_details and log['details'] else ""
                log_html += f'<div class="log-entry {status_class}">'
                log_html += f'[{log["timestamp"]}] <strong>[{log["agent"]}]</strong> {log["action"]}{details_str}'
                log_html += '</div>'
            log_html += '</div>'
            st.markdown(log_html, unsafe_allow_html=True)
            
            st.info(f"📊 Showing {len(filtered_logs)} of {len(st.session_state.agent_logs)} log entries")
        else:
            st.warning("No logs match the selected filters")
        
        # System Statistics
        st.markdown("---")
        st.markdown("### 📊 System Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Plans", st.session_state.system_stats['total_plans'])
        with col2:
            st.metric("Agents Run", st.session_state.system_stats['total_agents_run'])
        with col3:
            st.metric("Tasks Completed", st.session_state.system_stats['total_tasks_completed'])
        with col4:
            st.metric("Log Entries", len(st.session_state.agent_logs))
        
        # Session info
        st.markdown("---")
        st.markdown("### 🕐 Session Information")
        st.write(f"**Session Started:** {st.session_state.system_stats['session_start']}")
        st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Application logs from file
        st.markdown("---")
        st.markdown("### 📄 Application Logs")
        try:
            with open('trip_planner.log', 'r') as f:
                app_logs = f.read()
            st.text_area("Log File Contents", app_logs, height=200)
        except FileNotFoundError:
            st.info("No application log file found yet")
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Plan Another Trip", use_container_width=True):
        st.session_state.plan_generated = False
        st.session_state.current_plan = None
        logger.info("User initiated new plan generation")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="credit">
    <strong>✨ AI-Powered Trip Planner</strong><br>
    Developed by <a href="https://github.com/Ratnesh-181998" target="_blank">RATNESH SINGH</a> | Data Scientist<br>
    Powered by CrewAI & Ollama | © 2025
</div>
""", unsafe_allow_html=True)
