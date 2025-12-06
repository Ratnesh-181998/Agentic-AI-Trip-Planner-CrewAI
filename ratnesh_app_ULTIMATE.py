from TravelAgents import guide_expert, location_expert, planner_expert, booking_expert, get_llm
from TravelTasks import location_task, guide_task, planner_task, booking_task
from TravelTasks_LEGACY import location_task_legacy, guide_task_legacy, planner_task_legacy
from TravelTools import search_web_tool
from crewai import Crew, Process
import streamlit as st
from datetime import datetime
import os
import sys
import re
import base64
from io import StringIO

def get_img_src(image_path):
    """Convert local image path to base64 or return URL"""
    if str(image_path).startswith("http"):
        return image_path
    
    # It's a local file
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
    
    # Fallback to a placeholder or keep original if it might be valid relative path for server
    return image_path

def render_destination_cards(destinations):
    """Render destination cards with support for images and 5-sec video previews"""
    cols = st.columns(3)
    for idx, dest in enumerate(destinations):
        with cols[idx % 3]:
            # Check for video - if available, show video instead of image
            media_html = ""
            if 'video' in dest and dest['video']:
                 poster_src = get_img_src(dest['image'])
                 media_html = f"""
<video width="100%" height="200" autoplay loop muted playsinline poster="{poster_src}" style="object-fit: cover; border-radius: 12px 12px 0 0;">
    <source src="{dest['video']}" type="video/mp4">
    Your browser does not support the video tag.
</video>"""
            else:
                img_src = get_img_src(dest['image'])
                media_html = f'<img src="{img_src}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;" alt="{dest["name"]}">'
            
            st.markdown(f"""
<div class="destination-card">
    {media_html}
    <div style="padding: 15px;">
        <h3 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 20px;">{dest['name']}</h3>
        <p style="margin: 0 0 5px 0; color: #666; font-size: 13px;">{dest['country']}</p>
        <p style="margin: 0 0 10px 0; color: #555; font-size: 13px; font-style: italic;">{dest['description']}</p>
        <p style="margin: 5px 0; color: #333;"><strong style="color: #ff6b6b;">From:</strong> {dest['price']}</p>
        <p style="margin: 5px 0; color: #333;"><strong style="color: #4ecdc4;">Hotels:</strong> {dest['hotel']}</p>
    </div>
</div>""", unsafe_allow_html=True)

def render_history_tab(folder_path, category):
    """Render a history tab with card layout and black-tab content viewer"""
    st.header(f"📜 {category} Search History")
    st.markdown(f"*View and download your previously generated {category.lower()} options*")
    
    if not os.path.exists(folder_path):
        st.info(f"No {category.lower()} search history found yet. Perform a search to see results here!")
        return
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        st.info(f"No {category.lower()} search history found yet. Perform a search to see results here!")
        return
        
    # Sort files by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    
    st.success(f"📚 Found **{len(files)}** saved search(es)")
    
    # Display in grid
    cols_per_row = 2
    for i in range(0, len(files), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(files):
                filename = files[i + j]
                filepath = os.path.join(folder_path, filename)
                
                with cols[j]:
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        # Get metadata
                        timestamp = os.path.getmtime(filepath)
                        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        file_size_kb = os.path.getsize(filepath) / 1024
                        
                        # Icon map
                        icon_map = {"Flight": "\u2708\ufe0f", "Hotel": "\U0001f3e8", "Train": "\U0001f682", "Bus": "\U0001f68c"}
                        icon = icon_map.get(category, "\U0001f4c4")
                        
                        # Extract Details
                        from_loc = "Unknown"
                        to_loc = "Unknown"
                        
                        # 1. Try Structured Header (New Files)
                        if content.startswith("DETAILS"):
                             lines = content.split('\n')
                             for line in lines[:6]:
                                 if line.startswith("From:"):
                                     from_loc = line.split("From:")[1].strip()
                                 elif line.startswith("To:"):
                                     to_loc = line.split("To:")[1].strip()
                        
                        # 2. Fallback to Regex (Old Files) or if structured parsing failed
                        if from_loc == "Unknown" and to_loc == "Unknown":
                            # Standard pattern: "from [X] to [Y]"
                            match = re.search(r"(?:from|in)\s+([a-zA-Z\s,]+?)\s+to\s+([a-zA-Z\s,]+)", content[:500], re.IGNORECASE)
                            if match:
                                from_loc = match.group(1).strip().replace(":", "").replace("*", "")
                                to_loc = match.group(2).strip().split("\n")[0].split(".")[0].replace(":", "").replace("*", "")
                            elif category == "Hotel":
                                 # Hotel specific: "hotels in [City]"
                                match_hotel = re.search(r"hotels?\s+in\s+([a-zA-Z\s,]+)", content[:500], re.IGNORECASE)
                                if match_hotel:
                                    to_loc = match_hotel.group(1).strip().replace(":", "").replace("*", "")
                                    from_loc = "N/A"

                        # Clean up
                        if to_loc.lower() == "unknown" and category != "Hotel":
                             to_loc = f"{category} Search"
                        
                        # Try to find date in content
                        dates = "See Details"
                        
                        # Render Rich Card
                        # Render Rich Card
                        card_html = (
                            f'<div style="'
                            f'    border: 1px solid #e0e0e0;'
                            f'    border-radius: 12px;'
                            f'    padding: 15px;'
                            f'    margin-bottom: 15px;'
                            f'    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'
                            f'    color: white;'
                            f'    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'
                            f'">'
                            f'    <h3 style="margin: 0 0 10px 0; color: white; font-size: 1.2rem;">{icon} {to_loc if to_loc != "Unknown" else category + " Search"}</h3>'
                            f'    <div style="margin-left: 5px;">'
                            f'        <p style="margin: 3px 0; font-size: 14px; opacity: 0.95;"><strong>&#128205; From:</strong> {from_loc}</p>'
                            f'        <p style="margin: 3px 0; font-size: 14px; opacity: 0.95;"><strong>&#127937; To:</strong> {to_loc}</p>'
                            f'        <p style="margin: 3px 0; font-size: 14px; opacity: 0.95;"><strong>&#128197; Created:</strong> {date_str}</p>'
                            f'    </div>'
                            f'    <hr style="margin: 10px 0; opacity: 0.3;">'
                            f'    <p style="margin: 0; font-size: 12px; opacity: 0.8; font-style: italic;">{filename}</p>'
                            f'</div>'
                        )
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        with st.expander("👁️ View Details"):
                            st.code(content, language="markdown")
                        
                        st.download_button(
                            f"📥 Download", 
                            content, 
                            file_name=filename, 
                            key=f"dl_{filename}_{i}_{j}"
                        )
                    except Exception as e:
                        st.error(f"Error reading file {filename}: {e}")

def run_booking_crew(category, from_loc, to_loc, date, details):
    """Run the booking crew for a specific category with 5-Tier Fallback"""
    with st.spinner(f"🤖 AI Agent is searching for best {category} options..."):
        try:
            task = booking_task(
                agent=booking_expert,
                category=category,
                from_location=from_loc,
                to_location=to_loc,
                date=str(date),
                details=details
            )
            crew = Crew(
                agents=[booking_expert],
                tasks=[task],
                verbose=True,
                process=Process.sequential
            )
            result = crew.kickoff()
            
            # Check for silent errors from CrewAI/LLM returned as text
            result_str = str(result)
            if "Error: Invalid response" in result_str or "None or empty" in result_str:
                raise Exception(result_str)
                
            return result
        except Exception as e:
            error_msg = str(e).lower()
            # Broaden fallback triggers to include empty/invalid responses
            if "rate" in error_msg or "limit" in error_msg or "429" in error_msg or "invalid" in error_msg or "empty" in error_msg:
                 # High visibility alert for Tier 1 failure
                 st.markdown("""
                 <div style='background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.2);'>
                    🚨 Groq Rate Limit Hit! Engaging Emergency 5-Tier Fallback System...<br>
                    <span style='font-size: 0.9em; font-weight: normal;'>🔄 Switching to Tier 3: Google Gemini (Cloud Backup)</span>
                 </div>
                 """, unsafe_allow_html=True)
                 
                 try:
                     # Fallback to Google (Tier 3/4)
                     backup_llm = get_llm(force_google=True)
                     booking_expert.llm = backup_llm
                     # Re-create crew with updated agent
                     crew = Crew(agents=[booking_expert], tasks=[task], verbose=True)
                     return crew.kickoff()
                 except Exception as e2:
                     # High visibility alert for Tier 3 failure
                     st.markdown("""
                     <div style='background-color: #ffa500; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.2);'>
                        ⚠️ Cloud Fallback Failed! (Network/Auth Issue)<br>
                        <span style='font-size: 0.9em; font-weight: normal;'>🔄 Switching to Tier 5: Local Ollama (Offline Backup)</span>
                     </div>
                     """, unsafe_allow_html=True)
                     
                     # Fallback to Ollama (Tier 5)
                     backup_llm = get_llm(force_ollama=True)
                     booking_expert.llm = backup_llm
                     crew = Crew(agents=[booking_expert], tasks=[task], verbose=True)
                     return crew.kickoff()
            else:
                return f"Error: {str(e)}"


# Page config
st.set_page_config(page_title="AI Trip Planner", page_icon="\U0001f30d", layout="wide")

# Custom CSS for better styling including colorful sidebar
st.markdown("""
<style>
    /* Main app background with beautiful Earth/Nature theme - Sunrise/Sunset */
    .stApp {
        background: 
            linear-gradient(180deg, 
                #FFE5B4 0%,     /* Warm peach (sunrise sky) */
                #FFB88C 15%,    /* Soft coral */
                #87CEEB 35%,    /* Sky blue */
                #4A90E2 55%,    /* Ocean blue */
                #2E8B57 75%,    /* Sea green */
                #228B22 90%,    /* Forest green */
                #1B5E20 100%    /* Deep green (hills) */
            );
        background-attachment: fixed;
    }
    
    /* Main content area with light natural glassmorphism */
    .main .block-container {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Make text dark for light background */
    .main .block-container * {
        color: #2c3e50 !important;
    }
    
    /* Keep headers with gradient for visual interest */
    .main h1, .main h2, .main h3 {
        background: linear-gradient(90deg, #2E8B57 0%, #4A90E2 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    
    /* Add text shadows for better readability */
    .main p, .main span, .main div, .main label {
        text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.8) !important;
        font-weight: 500 !important;
    }
    
    /* Info/Alert boxes with better contrast */
    /* Info/Alert boxes with better contrast */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(0, 0, 0, 0.2) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Force text inside alerts to be black and visible - ULTRA SPECIFIC */
    .stAlert div, .stInfo div, .stSuccess div, .stWarning div, .stError div,
    .stAlert p, .stInfo p, .stSuccess p, .stWarning p, .stError p,
    div[data-baseweb="alert"] div, div[data-baseweb="alert"] p {
        color: #000000 !important;
        text-shadow: none !important;
        font-weight: 600 !important;
    }
    
    /* Make sure all text in main area is dark and visible */
    .main * {
        color: #1a1a1a !important;
    }
    
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        font-weight: 700 !important;
    }
    
    /* Image styling - ensure images load and display properly */
    img {
        max-width: 100% !important;
        height: auto !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%) !important;
        min-height: 200px !important;
        object-fit: cover !important;
    }
    
    /* Fallback for broken images */
    img[src=""], img:not([src]), img[src="#"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        display: block !important;
    }
    
    /* Sidebar styling with gradient background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 20px 10px;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 700;
    }
    
    /* Radio buttons styling */
    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Info boxes in sidebar */
    [data-testid="stSidebar"] .stAlert {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px);
    }
    
    /* Markdown in sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #f093fb;
        margin: 10px 0;
    }
    
    /* Main tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 15px;
        padding-right: 15px;
        font-size: 14px;
        font-weight: 600;
        background: linear-gradient(135deg, #e8eaf6 0%, #f3e5f5 100%);
        border-radius: 8px;
        transition: all 0.3s;
        color: #2c3e50 !important;
        border: 2px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        border-color: transparent;
    }
    .stTabs [data-baseweb="tab"]:hover * {
        color: white !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        border-color: transparent;
    }
    .stTabs [aria-selected="true"] * {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Buttons in sidebar */
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3) !important;
        transition: all 0.3s !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(245, 87, 108, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title with credit in top right corner
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px;">
        <div style="
            background: linear-gradient(135deg, #56CCF2 0%, #2F80ED 50%, #1CB5E0 100%);
            border-radius: 50%;
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px rgba(86, 204, 242, 0.5);
            font-size: 50px;
        ">
            &#127757;
        </div>
        <h1 style="
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 48px;
            font-weight: 800;
            margin: 0;
            padding: 0;
        ">
            AGENTIC AI Trip Planner
        </h1>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="
        text-align: right;
        padding: 15px 20px;
        margin-top: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.3);
    ">
        <p style="margin: 0; line-height: 1.6;">
            <strong style="
                color: #ffffff;
                font-size: 16px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">By Ratnesh Singh</strong><br>
            <span style="
                font-size: 13px;
                color: #f0f0f0;
                font-weight: 500;
                letter-spacing: 0.5px;
            ">Data Scientist | 4+ Year Exp</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Create main tabs
tab1, tab_history, tab2, tab3, tab3_hist, tab4, tab4_hist, tab5, tab5_hist, tab6, tab6_hist, tab7, tab8 = st.tabs([
    "\U0001f916 AI Trip Planner",
    "\U0001f4dc AI Trip Planner History",
    "\U0001f3af Explore by Interest",
    "\u2708\ufe0f Flights",
    "\U0001f4dc Flight History",
    "\U0001f3e8 Hotels",
    "\U0001f4dc Hotel History",
    "\U0001f682 Trains",
    "\U0001f4dc Train History",
    "\U0001f68c Buses",
    "\U0001f4dc Bus History",
    "\U0001f31f Destinations",
    "\U0001f4a1 Travel Tips"
])

# ============================================================================
# TAB 1: AI TRIP PLANNER (Complete functionality from SINGLE_PAGE)
# ============================================================================
with tab1:
    st.markdown("""
    &#128161; **Plan your next trip with AI!**  
    Enter your travel details below, and our AGENTIC AI travel assistant will create a personalized itinerary including:
     Best places to visit &#127905;   Accommodation & budget planning &#128176;
     Local food recommendations &#127829;   Transportation & visa details &#128646;
    """)
    
    # Default setting for Ollama fallback
    allow_ollama = False
    
    # Sidebar - LLM Configuration
    with st.sidebar:
        st.header("\u2699\ufe0f Settings")
        
        st.subheader("\U0001f916 AI Model Configuration")
        llm_choice = st.radio(
            "Choose LLM Provider:",
            ["Auto (5-Tier Fallback)", "Groq Only", "Google Only", "Ollama Only"],
            help="Auto mode tries multiple providers for maximum reliability"
        )
        
        if llm_choice == "Auto (5-Tier Fallback)":
            st.success("\u2705 Smart mode: Maximum reliability with 5 fallback options!")
        elif llm_choice == "Groq Only":
            st.warning("\u26a1 Fast but requires API key and internet")
        elif llm_choice == "Google Only":
            st.info("\U0001f31f Uses Google Gemini models (2.0 Flash \u2192 1.5 Pro)")
        else:
            st.warning("\U0001f40c Slower but works offline (requires Ollama running)")
        
        st.markdown("---")
        st.markdown("### &#128259; **5-Tier Fallback System**")
        st.markdown(
            "**Tier 1:** Groq llama-3.3-70b (Highest Quality)\\n\\n"
            "**Tier 2:** Groq llama-3.1-8b (Fast Lightweight)\\n\\n"
            "**Tier 3:** Groq mixtral-8x7b (High Quality Alternative)\\n\\n"
            "**Tier 4:** Groq gemma2-9b (Google's Open Model)\\n\\n"
            "**Tier 5:** Ollama llama3.2 (Local Offline Backup)"
        )
        
        # Add checkbox for Ollama fallback
        st.markdown("---")
        allow_ollama = st.checkbox(
            "\U0001f40c Allow Local Ollama Fallback",
            value=True,
            help="Enable Tier 5 (Ollama) as final fallback. Slower but works offline."
        )
    
    # List of popular countries
    countries = [
        "India", "United States", "United Kingdom", "Canada", "Australia",
        "Japan", "China", "Singapore", "Thailand", "Malaysia",
        "Indonesia", "Vietnam", "South Korea", "UAE", "Saudi Arabia",
        "France", "Germany", "Italy", "Spain", "Switzerland",
        "Netherlands", "Belgium", "Austria", "Greece", "Turkey",
        "Egypt", "South Africa", "Kenya", "Morocco", "Brazil",
        "Argentina", "Mexico", "Peru", "Chile", "Russia",
        "New Zealand", "Fiji", "Maldives", "Sri Lanka", "Nepal",
        "Bhutan", "Myanmar", "Cambodia", "Laos", "Philippines",
        "Hong Kong", "Macau", "Taiwan", "Portugal", "Ireland"
    ]
    
    # Popular cities by country
    cities_by_country = {
        "India": ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Goa"],
        "United States": ["New York", "Los Angeles", "San Francisco", "Las Vegas", "Miami", "Chicago", "Boston", "Seattle", "Orlando", "Washington DC"],
        "United Kingdom": ["London", "Manchester", "Edinburgh", "Birmingham", "Liverpool", "Oxford", "Cambridge", "Bath", "York", "Brighton"],
        "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Quebec City", "Niagara Falls", "Banff", "Victoria", "Whistler"],
        "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Cairns", "Hobart", "Darwin", "Canberra"],
        "Japan": ["Tokyo", "Kyoto", "Osaka", "Hiroshima", "Nara", "Yokohama", "Sapporo", "Fukuoka", "Nagoya", "Kobe"],
        "China": ["Beijing", "Shanghai", "Hong Kong", "Guangzhou", "Shenzhen", "Chengdu", "Xi'an", "Hangzhou", "Suzhou", "Macau"],
        "Singapore": ["Singapore"],
        "Thailand": ["Bangkok", "Phuket", "Chiang Mai", "Pattaya", "Krabi", "Koh Samui", "Ayutthaya", "Hua Hin", "Koh Phi Phi", "Chiang Rai"],
        "Malaysia": ["Kuala Lumpur", "Penang", "Langkawi", "Malacca", "Johor Bahru", "Kota Kinabalu", "Cameron Highlands", "Ipoh", "Genting Highlands", "Kuching"],
        "France": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux", "Strasbourg", "Toulouse", "Cannes", "Monaco", "Versailles"],
        "Italy": ["Rome", "Venice", "Florence", "Milan", "Naples", "Pisa", "Verona", "Bologna", "Turin", "Genoa"],
        "Spain": ["Barcelona", "Madrid", "Seville", "Valencia", "Granada", "Bilbao", "Malaga", "Ibiza", "Mallorca", "Toledo"],
        "UAE": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Al Ain"],
        "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Stuttgart", "Dresden", "Heidelberg", "Nuremberg", "Leipzig"],
        "Switzerland": ["Zurich", "Geneva", "Lucerne", "Interlaken", "Bern", "Zermatt", "Lausanne", "Basel", "Montreux", "St. Moritz"],
        "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", "Groningen", "Maastricht", "Delft", "Haarlem", "Leiden"],
        "Turkey": ["Istanbul", "Ankara", "Antalya", "Izmir", "Cappadocia", "Bodrum", "Pamukkale", "Ephesus", "Fethiye", "Marmaris"],
        "Egypt": ["Cairo", "Alexandria", "Luxor", "Aswan", "Hurghada", "Sharm El Sheikh", "Giza", "Dahab", "Marsa Alam", "Port Said"],
        "Maldives": ["Male", "Hulhumale", "Maafushi", "Addu City"],
        "Sri Lanka": ["Colombo", "Kandy", "Galle", "Nuwara Eliya", "Sigiriya", "Ella", "Anuradhapura", "Trincomalee", "Jaffna", "Bentota"],
        "Nepal": ["Kathmandu", "Pokhara", "Lumbini", "Chitwan", "Nagarkot", "Bhaktapur", "Patan", "Bandipur"],
        "Indonesia": ["Bali", "Jakarta", "Yogyakarta", "Lombok", "Bandung", "Surabaya", "Ubud", "Gili Islands", "Borobudur", "Komodo"],
        "Vietnam": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hoi An", "Nha Trang", "Halong Bay", "Hue", "Sapa", "Dalat", "Phu Quoc"],
        "South Korea": ["Seoul", "Busan", "Jeju Island", "Incheon", "Gyeongju", "Daegu", "Suwon", "Jeonju", "Sokcho", "Andong"],
        "New Zealand": ["Auckland", "Queenstown", "Wellington", "Christchurch", "Rotorua", "Dunedin", "Taupo", "Nelson", "Wanaka", "Hamilton"],
        "Brazil": ["Rio de Janeiro", "Sao Paulo", "Brasilia", "Salvador", "Fortaleza", "Manaus", "Recife", "Florianopolis", "Foz do Iguacu", "Belo Horizonte"],
        "Mexico": ["Mexico City", "Cancun", "Playa del Carmen", "Tulum", "Guadalajara", "Monterrey", "Puerto Vallarta", "Cabo San Lucas", "Oaxaca", "Merida"],
        "South Africa": ["Cape Town", "Johannesburg", "Durban", "Pretoria", "Port Elizabeth", "Kruger National Park", "Stellenbosch", "Knysna", "Hermanus", "Sun City"],
        "Greece": ["Athens", "Santorini", "Mykonos", "Crete", "Rhodes", "Corfu", "Thessaloniki", "Zakynthos", "Naxos", "Paros"],
        "Portugal": ["Lisbon", "Porto", "Algarve", "Madeira", "Sintra", "Coimbra", "Evora", "Braga", "Cascais", "Azores"],
        "Ireland": ["Dublin", "Cork", "Galway", "Killarney", "Belfast", "Limerick", "Waterford", "Kilkenny", "Dingle", "Cliffs of Moher"],
    }
    
    # From Country and City
    col1, col2 = st.columns(2)
    with col1:
        from_country = st.selectbox("\U0001f3e1 From Country", countries, index=0)
    with col2:
        from_cities = cities_by_country.get(from_country, [from_country])
        from_city = st.selectbox("\U0001f3d9\ufe0f From City", from_cities, index=0)
    
    # Destination Country and City
    col3, col4 = st.columns(2)
    with col3:
        dest_country = st.selectbox("✈️ Destination Country", countries, index=5)  # Default to Japan
    with col4:
        dest_cities = cities_by_country.get(dest_country, [dest_country])
        destination_city = st.selectbox("🌆 Destination City", dest_cities, index=0)
    
    # Dates
    col5, col6 = st.columns(2)
    with col5:
        date_from = st.date_input("📅 Departure Date")
    with col6:
        date_to = st.date_input("📅 Return Date")
    
    # Person Count
    st.markdown("### 👥 Number of Travelers")
    col1, col2 = st.columns(2)
    with col1:
        num_adults = st.number_input("👨 Adults (18+ years)", min_value=1, max_value=10, value=2, step=1)
    with col2:
        num_children = st.number_input("👶 Children (0-18 years)", min_value=0, max_value=10, value=0, step=1)
    
    total_persons = num_adults + num_children
    st.info(f"**Total Travelers:** {total_persons} person(s) - {num_adults} adult(s) + {num_children} child(ren)")
    
    # Interests
    st.markdown("### 🎯 Your Interests")
    interest_options = [
        "🏛️ Sightseeing & Landmarks",
        "🍕 Food & Dining",
        "🎨 Art & Museums",
        "🏖️ Beach & Relaxation",
        "⛰️ Adventure & Hiking",
        "🎭 Culture & History",
        "🛍️ Shopping",
        "🎉 Nightlife & Parties",
        "📸 Photography",
        "🏃 Sports & Fitness",
        "🧘 Wellness & Spa",
        "🎪 Entertainment & Shows",
        "🌳 Nature & Wildlife",
        "🏰 Architecture",
        "🍷 Wine & Gastronomy",
        "🎵 Music & Concerts",
        "👨‍👩‍👧 Family Activities",
        "💑 Romantic Experiences",
        "🎓 Educational Tours",
        "🚴 Cycling & Biking",
        "⛷️ Winter Sports",
        "🏄 Water Sports",
        "🎮 Gaming & Technology",
        "🌆 Urban Exploration"
    ]
    
    selected_interests = st.multiselect(
        "Select your travel interests (choose multiple):",
        interest_options,
        default=["🏛️ Sightseeing & Landmarks", "🍕 Food & Dining"]
    )
    
    # Convert selected interests to a comma-separated string
    if selected_interests:
        interests = ", ".join([interest.split(" ", 1)[1] for interest in selected_interests])  # Remove emoji
    else:
        interests = "sightseeing and good food"
    
    st.info(f"**Selected Interests:** {interests}")
    
    # Button to run CrewAI
    if st.button("🚀 Generate Travel Plan"):
        if not from_city or not destination_city or not date_from or not date_to or not interests:
            st.error("⚠️ Please fill in all fields before generating your travel plan.")
        else:
            st.write("⏳ AI is preparing your personalized travel itinerary... Please wait.")

            # Create outputs directory if it doesn't exist
            output_dir = "trip_plans"
            os.makedirs(output_dir, exist_ok=True)

            # Handle LLM provider selection
            if llm_choice == "Google Only":
                # Force Google models only
                from TravelAgents import get_llm
                from crewai import Agent
                
                st.info("🌟 Using Google Gemini models...")
                google_llm = get_llm(force_google=True)
                
                # Recreate agents with Google LLM
                location_expert_google = Agent(
                    role="Travel Logistics & Information Specialist",
                    goal="Research and provide comprehensive travel information including transportation, accommodations, costs, weather, and visa requirements.",
                    backstory="""You are an experienced travel consultant with 15 years of expertise in planning 
                    domestic and international trips. You excel at finding the best transportation options, 
                    accommodation deals, and providing accurate cost estimates. You always provide complete, 
                    detailed reports with specific recommendations and pricing.""",
                    tools=[search_web_tool],
                    verbose=True,
                    max_iter=15,
                    llm=google_llm,
                    allow_delegation=False,
                )
                
                guide_expert_google = Agent(
                    role="Local Guide & Attractions Specialist",
                    goal="Discover and recommend the best attractions, restaurants, activities, and events based on traveler interests.",
                    backstory="You are a passionate local guide who has lived in major cities across the world. You know the hidden gems, best restaurants, must-visit attractions, and exciting events. You tailor recommendations to match traveler interests perfectly, whether it's sightseeing, food, adventure, or nightlife. You always provide specific names, addresses, and insider tips.",
                    tools=[search_web_tool],
                    verbose=True,
                    max_iter=15,
                    llm=google_llm,
                    allow_delegation=False,
                )
                
                planner_expert_google = Agent(
                    role="Master Itinerary Planner",
                    goal="Create detailed, day-by-day travel itineraries with specific timings, activities, and budget breakdowns.",
                    backstory="""You are a professional travel planner who has created over 1000 successful 
                    itineraries. You excel at organizing information into clear, actionable day-by-day plans 
                    with specific timings, realistic travel times, and accurate budget estimates. You always 
                    include a city introduction, detailed daily schedules, restaurant recommendations, and 
                    practical tips. Your itineraries are comprehensive, well-structured, and easy to follow.""",
                    tools=[search_web_tool],
                    verbose=True,
                    max_iter=20,
                    llm=google_llm,
                    allow_delegation=False,
                )
                
                # Use Google agents
                # Use LEGACY tasks for detailed output
                loc_task = location_task_legacy(location_expert_google, from_city, destination_city, date_from, date_to, num_adults, num_children)
                guid_task = guide_task_legacy(guide_expert_google, destination_city, interests, date_from, date_to)
                plan_task = planner_task_legacy([loc_task, guid_task], planner_expert_google, destination_city, interests, date_from, date_to, num_adults, num_children)
                
                crew = Crew(
                    agents=[location_expert_google, guide_expert_google, planner_expert_google],
                    tasks=[loc_task, guid_task, plan_task],
                    process=Process.sequential,
                    full_output=False,
                    verbose=True,
                )
            else:
                # Use default agents (Auto/Groq/Ollama modes)
                # Use LEGACY tasks for detailed output
                loc_task = location_task_legacy(location_expert, from_city, destination_city, date_from, date_to, num_adults, num_children)
                guid_task = guide_task_legacy(guide_expert, destination_city, interests, date_from, date_to)
                plan_task = planner_task_legacy([loc_task, guid_task], planner_expert, destination_city, interests, date_from, date_to, num_adults, num_children)
                
                crew = Crew(
                    agents=[location_expert, guide_expert, planner_expert],
                    tasks=[loc_task, guid_task, plan_task],
                    process=Process.sequential,
                    full_output=False,
                    verbose=True,
                )

            # Run Crew AI with TRUE 5-TIER CASCADING FALLBACK
            result = None
            console_output = StringIO()  # Capture console output
            old_stdout = sys.stdout
            successful_tier = None
            
            # Show 5-tier system status with OPTIMIZED path
            st.info("🔄 **Smart Fallback System Active**")
            st.markdown(
                "**Optimization Strategy:**\n\n"
                "- **1. Groq llama-3.3-70b**: Highest Quality (Primary) ⚡⚡⚡\n"
                "- **2. Groq llama-3.1-8b**: Fast Lightweight Backup ⚡⚡\n"
                "- **3. Groq mixtral-8x7b**: High Quality Alternative ⚡⚡\n"
                "- **4. Groq gemma2-9b**: Google's Open Model (on Groq) ⚡⚡\n"
                "- **5. Ollama llama3.2**: Offline/Local Backup 🐌"
            )
            
            # Define all 5 tiers with their configurations
            tiers = [
                {
                    "name": "Groq llama-3.3-70b",
                    "tier": 1,
                    "model": "groq/llama-3.3-70b-versatile",
                    "api_key_env": "GROQ_API_KEY",
                    "emoji": "⚡⚡⚡",
                    "time": "1-3 minutes"
                },
                {
                    "name": "Groq llama-3.1-8b",
                    "tier": 2,
                    "model": "groq/llama-3.1-8b-instant",
                    "api_key_env": "GROQ_API_KEY",
                    "emoji": "⚡⚡",
                    "time": "1-2 minutes"
                },
                {
                    "name": "Groq mixtral-8x7b",
                    "tier": 3,
                    "model": "groq/mixtral-8x7b-32768",
                    "api_key_env": "GROQ_API_KEY",
                    "emoji": "⚡⚡",
                    "time": "1-3 minutes"
                },
                {
                    "name": "Groq gemma2-9b",
                    "tier": 4,
                    "model": "groq/gemma2-9b-it",
                    "api_key_env": "GROQ_API_KEY",
                    "emoji": "⚡⚡",
                    "time": "1-2 minutes"
                },
                {
                    "name": "Ollama llama3.2 (Local)",
                    "tier": 5,
                    "model": "ollama/llama3.2",
                    "api_key_env": None,
                    "emoji": "🐌",
                    "time": "5-15 minutes",
                    "base_url": "http://localhost:11434",
                    "timeout": 3000
                }
            ]
            
            # Try each tier sequentially
            for tier_config in tiers:
                tier_num = tier_config["tier"]
                tier_name = tier_config["name"]
                
                # SKIP Tier 5 (Ollama) if not allowed by user
                if tier_num == 5 and not allow_ollama:
                     continue

                # Skip if API key is required but not available
                if tier_config["api_key_env"]:
                    api_key = os.getenv(tier_config["api_key_env"])
                    if not api_key or api_key == "your-groq-api-key-here" or api_key == "your-google-api-key-here":
                         # st.warning(f"⚠️ **[TIER {tier_num}]** Skipping {tier_name} - No API key found")
                        continue
                
                try:
                    st.info(f"🚀 **[TIER {tier_num}]** Trying {tier_name} {tier_config['emoji']} (~{tier_config['time']})...")
                    # No waiting here anymore 

                    # Redirect stdout to capture console output
                    sys.stdout = console_output
                    
                    # Create LLM for this tier
                    from crewai import LLM, Agent

                    if tier_num == 5:  # Ollama
                        tier_llm = LLM(
                            model=tier_config["model"],
                            base_url=tier_config["base_url"],
                            timeout=tier_config.get("timeout", 1800)
                        )
                    else:  # Cloud providers
                        tier_llm = LLM(
                            model=tier_config["model"],
                            api_key=api_key
                        )
                    
                    # Create agents with this tier's LLM
                    location_expert_tier = Agent(
                        role="Travel Logistics & Information Specialist",
                        goal="Research and provide comprehensive travel information including transportation, accommodations, costs, weather, and visa requirements.",
                        backstory="You are an experienced travel consultant with 15 years of expertise in planning domestic and international trips. You excel at finding the best transportation options, accommodation deals, and providing accurate cost estimates. You always provide complete, detailed reports with specific recommendations and pricing.",
                        tools=[search_web_tool],
                        verbose=True,
                        max_iter=15,
                        llm=tier_llm,
                        allow_delegation=False,
                    )
                    
                    guide_expert_tier = Agent(
                        role="Local Guide & Attractions Specialist",
                        goal="Discover and recommend the best attractions, restaurants, activities, and events based on traveler interests.",
                        backstory="You are a passionate local guide who has lived in major cities across the world. You know the hidden gems, best restaurants, must-visit attractions, and exciting events. You tailor recommendations to match traveler interests perfectly, whether it's sightseeing, food, adventure, or nightlife. You always provide specific names, addresses, and insider tips.",
                        tools=[search_web_tool],
                        verbose=True,
                        max_iter=15,
                        llm=tier_llm,
                        allow_delegation=False,
                    )
                    
                    planner_expert_tier = Agent(
                        role="Master Itinerary Planner",
                        goal="Create detailed, day-by-day travel itineraries with specific timings, activities, and budget breakdowns.",
                        backstory="You are a professional travel planner who has created over 1000 successful itineraries. You excel at organizing information into clear, actionable day-by-day plans with specific timings, realistic travel times, and accurate budget estimates. You always include a city introduction, detailed daily schedules, restaurant recommendations, and practical tips. Your itineraries are comprehensive, well-structured, and easy to follow.",
                        tools=[search_web_tool],
                        verbose=True,
                        max_iter=20,
                        llm=tier_llm,
                        allow_delegation=False,
                    )
                    
                    # Create tasks using LEGACY definitions for detailed output
                    loc_task_tier = location_task_legacy(location_expert_tier, from_city, destination_city, date_from, date_to, num_adults, num_children)
                    guid_task_tier = guide_task_legacy(guide_expert_tier, destination_city, interests, date_from, date_to)
                    plan_task_tier = planner_task_legacy([loc_task_tier, guid_task_tier], planner_expert_tier, destination_city, interests, date_from, date_to, num_adults, num_children)
                    
                    # Create crew
                    crew_tier = Crew(
                        agents=[location_expert_tier, guide_expert_tier, planner_expert_tier],
                        tasks=[loc_task_tier, guid_task_tier, plan_task_tier],
                        process=Process.sequential,
                        full_output=False,
                        verbose=True,
                    )
                    
                    # Execute
                    result = crew_tier.kickoff()
                    
                    # Restore stdout
                    sys.stdout = old_stdout
                    
                    # Success!
                    successful_tier = tier_num
                    st.success(f"\u2705 **[TIER {tier_num}]** Completed using {tier_name}!")
                    break  # Exit loop on success
                    
                except Exception as e:
                    # Restore stdout
                    sys.stdout = old_stdout
                    
                    error_msg = str(e)
                    # High-visibility Error Alert
                    st.markdown(
                        f"<div style='background-color: #ffa500; color: white; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.2);'>"
                        f"   [TIER {tier_num}] {tier_name} Failed!<br>"
                        f"   <span style='font-size: 0.9em; font-weight: normal;'>{error_msg[:100]}...</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    
                    # If this is the last tier, re-raise the error
                    if tier_num == 5:
                        st.error("\u274c All 5 tiers failed! Please check your API keys and Ollama installation.")
                        raise
                    else:
                        # Continue to next tier with High-Vis Alert
                        st.markdown(
                            f"<div style='background-color: #3182ce; color: white; padding: 10px; border-radius: 10px; font-weight: bold; text-align: center; margin: 5px 0;'>"
                            f"   [TIER {tier_num + 1}] Switching to Next Tier..."
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        continue
            
            # If we get here without a result, something went wrong
            # If we get here without a result, something went wrong
            if result is None:
                if not allow_ollama:
                     st.error("\u274c All Cloud LLMs failed and Local Ollama Fallback is disabled.")
                     st.info("\U0001f4a1 **Tips to fix:**")
                     st.markdown(
                         "1. **Wait 2-3 minutes** for Groq rate limits to reset (most likely cause).\n"
                         "2. Enable **'&#128012; Allow Local Ollama Fallback'** in the sidebar (slow but works).\n"
                         "3. Check your `GOOGLE_API_KEY` in `.env` if you have one."
                     )
                     st.stop()
                else:
                    raise Exception("\u274c All LLM tiers failed to generate a response! Please check your API keys and internet connection.")

            # Get captured console output
            captured_logs = console_output.getvalue()

            # Create detailed log with all information
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_content = []
            
            log_content.append("="*80)
            log_content.append("AI TRIP PLANNER - EXECUTION LOG")
            log_content.append("="*80)
            log_content.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            log_content.append(f"\n{'='*80}\n")
            
            log_content.append("TRIP DETAILS:")
            log_content.append(f"  From: {from_city}")
            log_content.append(f"  Destination: {destination_city}")
            log_content.append(f"  Departure Date: {date_from}")
            log_content.append(f"  Return Date: {date_to}")
            log_content.append(f"  Travelers: {num_adults} adults + {num_children} children")
            log_content.append(f"  Interests: {interests}")
            log_content.append(f"\n{'='*80}\n")
            
            # Add captured console output
            if captured_logs:
                log_content.append("DETAILED EXECUTION LOG:")
                log_content.append("="*80)
                log_content.append(captured_logs)
                log_content.append(f"\n{'='*80}\n")
            
            log_content.append(f"\n{'='*80}\n")
            log_content.append("FINAL TRAVEL PLAN:")
            log_content.append("="*80)
            log_content.append(str(result))
            log_content.append(f"\n{'='*80}\n")
            log_content.append(f"End of Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            log_content.append("="*80)
            
            # Join all content
            full_log_raw = "\n".join(log_content)
            
            # Function to strip ANSI codes (colors)
            plain_log = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', full_log_raw)
            
            # Save to file with timestamp

            filename = f"TripPlan_{destination_city.replace(' ', '_')}_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(plain_log)
            
            st.success(f"✅ Travel plan saved to: {filepath}")

            # Display Results
            st.subheader("✅ Your AGENTIC AITravel Plan")
            with st.expander("👁️ View Formatted Plan", expanded=True):
                st.code(result, language="markdown")

            with st.expander("🔍 View Research & Log (Search Details)", expanded=False):
                st.text_area("Execution Log", captured_logs, height=400)

            # Download button
            st.download_button(
                label="📥 Download Travel Plan",
                data=plain_log,
                file_name=f"Travel_Plan_{destination_city}_{timestamp}.txt",
                mime="text/plain"
            )


# ============================================================================
# TAB: AI TRIP PLANNER HISTORY (Display all saved trip plans)
# ============================================================================
with tab_history:
    st.header("📜 AI Trip Planner History")
    st.markdown("*View and download your previously generated trip plans*")
    
    # Get all trip plan files
    trip_plans_dir = "trip_plans"
    
    if not os.path.exists(trip_plans_dir):
        st.info("🚫 No travel history found. Generate your first trip plan in the AI Trip Planner tab!")
    else:
        # Get all .txt files from trip_plans directory
        trip_files = [f for f in os.listdir(trip_plans_dir) if f.endswith('.txt')]
        
        if len(trip_files) == 0:
            st.info("🚫 No travel history found. Generate your first trip plan in the AI Trip Planner tab!")
        else:
            st.success(f"📚 Found **{len(trip_files)}** saved trip plan(s)")
            
            # Sort files by modification time (newest first)
            trip_files.sort(key=lambda x: os.path.getmtime(os.path.join(trip_plans_dir, x)), reverse=True)
            
            # Display trip plans in a grid
            cols_per_row = 2
            for i in range(0, len(trip_files), cols_per_row):
                cols = st.columns(cols_per_row)
                
                for j in range(cols_per_row):
                    if i + j < len(trip_files):
                        filename = trip_files[i + j]
                        filepath = os.path.join(trip_plans_dir, filename)
                        
                        with cols[j]:
                            # Read file to extract trip details
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # Extract trip details from the file
                                destination = "Unknown"
                                from_city = "Unknown"
                                date_from = "N/A"
                                date_to = "N/A"
                                travelers = "N/A"
                                interests = "N/A"
                                generated_date = "N/A"
                                
                                # Parse the content
                                lines = content.split('\n')
                                for idx, line in enumerate(lines):
                                    if "Generated:" in line:
                                        generated_date = line.split("Generated:")[1].strip()
                                    elif "From:" in line and "TRIP DETAILS" in content[max(0, content.index(line)-200):content.index(line)]:
                                        from_city = line.split("From:")[1].strip()
                                    elif "Destination:" in line and "TRIP DETAILS" in content[max(0, content.index(line)-200):content.index(line)]:
                                        destination = line.split("Destination:")[1].strip()
                                    elif "Departure Date:" in line:
                                        date_from = line.split("Departure Date:")[1].strip()
                                    elif "Return Date:" in line:
                                        date_to = line.split("Return Date:")[1].strip()
                                    elif "Travelers:" in line and "adults" in line:
                                        travelers = line.split("Travelers:")[1].strip()
                                    elif "Interests:" in line and "TRIP DETAILS" in content[max(0, content.index(line)-300):content.index(line)]:
                                        interests = line.split("Interests:")[1].strip()
                                
                                # Get file size
                                file_size = os.path.getsize(filepath)
                                file_size_kb = file_size / 1024
                                
                                # Create a beautiful card
                                st.markdown(
                                    f'<div style="border: 2px solid #e0e0e0; border-radius: 15px; padding: 20px; margin-bottom: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.3s;">'
                                    f'<h3 style="margin: 0 0 10px 0; color: white; font-size: 22px;">✈️ {destination}</h3>'
                                    f'<p style="margin: 5px 0; font-size: 14px; opacity: 0.9;"><strong>📍 From:</strong> {from_city}</p>'
                                    f'<p style="margin: 5px 0; font-size: 14px; opacity: 0.9;"><strong>📅 Dates:</strong> {date_from} → {date_to}</p>'
                                    f'<p style="margin: 5px 0; font-size: 14px; opacity: 0.9;"><strong>👥 Travelers:</strong> {travelers}</p>'
                                    f'<p style="margin: 5px 0; font-size: 14px; opacity: 0.9;"><strong>🎯 Interests:</strong> {interests[:50]}...</p>'
                                    f'<hr style="border: 1px solid rgba(255,255,255,0.3); margin: 15px 0;">'
                                    f'<p style="margin: 5px 0; font-size: 12px; opacity: 0.8;"><strong>📅 Generated:</strong> {generated_date}</p>'
                                    f'<p style="margin: 5px 0; font-size: 12px; opacity: 0.8;"><strong>📄 Size:</strong> {file_size_kb:.1f} KB</p>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )
                                
                                # Action buttons
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # View button
                                    if st.button(f"👁️ View", key=f"view_{filename}"):
                                        st.session_state[f"show_{filename}"] = not st.session_state.get(f"show_{filename}", False)
                                
                                with col2:
                                    # Download button
                                    st.download_button(
                                        label="📥 Download",
                                        data=content,
                                        file_name=filename,
                                        mime="text/plain",
                                        key=f"download_{filename}"
                                    )
                                
                                # Show content if view button was clicked
                                if st.session_state.get(f"show_{filename}", False):
                                    with st.expander("📖 Trip Plan Details", expanded=True):
                                        # Extract and display the final travel plan (skip the execution logs)
                                        if "FINAL TRAVEL PLAN:" in content:
                                            plan_start = content.index("FINAL TRAVEL PLAN:")
                                            plan_content = content[plan_start:]
                                            
                                            # Remove the header and footer
                                            plan_lines = plan_content.split('\n')
                                            clean_plan = []
                                            skip_next = False
                                            for line in plan_lines:
                                                if "=" * 20 in line or "FINAL TRAVEL PLAN" in line or "End of Report" in line:
                                                    continue
                                                # Remove ANSI color codes
                                                clean_line = line
                                                import re
                                                clean_line = re.sub(r'\x1b\[[0-9;]*m', '', clean_line)
                                                if clean_line.strip():
                                                    clean_plan.append(clean_line)
                                            
                                            st.markdown("\\n".join(clean_plan[:100]))  # Show first 100 lines
                                            
                                            if len(clean_plan) > 100:
                                                st.info(f"📄 Showing first 100 lines. Download the full plan to see everything!")
                                        else:
                                            st.text(content[:2000])  # Show first 2000 characters
                                            if len(content) > 2000:
                                                st.info("📄 Content truncated. Download the full plan to see everything!")
                                
                            except Exception as e:
                                st.error(f"❌ Error reading file: {str(e)}")
                                st.markdown(
                                    f'<div style="border: 2px solid #ff6b6b; border-radius: 15px; padding: 20px; margin-bottom: 20px; background: #ffe0e0;">'
                                    f'<h4 style="color: #c92a2a;">⚠️ Error Loading Trip Plan</h4>'
                                    f'<p style="color: #666;">{filename}</p>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )

# ============================================================================
# TAB 2: EXPLORE BY INTEREST (From INTEREST_TABS)
# ============================================================================
with tab2:
    st.header("🎯 Explore Destinations by Interest")
    
    # Create sub-tabs for each interest category
    interest_tabs = st.tabs([
        "🙏 Religious",
        "🎭 Cultural", 
        "🌳 Nature",
        "🍕 Food",
        "🎉 Festivals",
        "🏛️ Historical",
        "🛍️ Shopping",
        "🏖️ Beaches",
        "⛰️ Mountains",
        "🏕️ Outdoors",
        "🎊 Nightlife",
        "💎 Luxury",
        "🧘 Wellness",
        "💑 Romance",
        "✨ Night Skies",
        "⚽ Sports",
        "🌟 Offbeat"
    ])
    
    # RELIGIOUS DESTINATIONS
    with interest_tabs[0]:
        st.markdown("### 🙏 Best Religious & Spiritual Destinations")
        st.markdown("*Discover sacred sites, temples, churches, and spiritual retreats*")
        
        religious_destinations = [
            {
                "name": "Varanasi",
                "country": "India",
                "description": "Ancient holy city on the Ganges, spiritual capital of India",
                "price": "₹5K",
                "hotel": "₹2,000/night",
                "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400&h=250&fit=crop"
            },
            {
                "name": "Jerusalem",
                "country": "Israel",
                "description": "Sacred city for Judaism, Christianity, and Islam",
                "price": "₹60K",
                "hotel": "₹15,000/night",
                "image": "images/jerusalem.png"
            },
            {
                "name": "Mecca",
                "country": "Saudi Arabia",
                "description": "Holiest city in Islam, destination for Hajj pilgrimage",
                "price": "₹80K",
                "hotel": "₹20,000/night",
                "image": "https://images.unsplash.com/photo-1591604129939-f1efa4d9f7fa?w=400&h=250&fit=crop"
            },
            {
                "name": "Vatican City",
                "country": "Vatican",
                "description": "Center of Roman Catholic Church, home to the Pope",
                "price": "₹45K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1531572753322-ad063cecc140?w=400&h=250&fit=crop"
            },
            {
                "name": "Bodh Gaya",
                "country": "India",
                "description": "Where Buddha attained enlightenment, major Buddhist pilgrimage site",
                "price": "₹8K",
                "hotel": "₹2,500/night",
                "image": "https://images.unsplash.com/photo-1548013146-72479768bada?w=400&h=250&fit=crop"
            },
            {
                "name": "Kyoto Temples",
                "country": "Japan",
                "description": "Over 2000 temples and shrines, spiritual heart of Japan",
                "price": "₹30K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(religious_destinations)
    
    # CULTURAL DESTINATIONS
    with interest_tabs[1]:
        st.markdown("### 🎭 Best Cultural Destinations")
        st.markdown("*Immerse yourself in art, music, theater, and local traditions*")
        
        cultural_destinations = [
            {
                "name": "Paris",
                "country": "France",
                "description": "Art capital with Louvre, museums, and French culture",
                "price": "₹35K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=250&fit=crop"
            },
            {
                "name": "Kyoto",
                "country": "Japan",
                "description": "Traditional Japanese culture, geishas, tea ceremonies",
                "price": "₹28K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&h=250&fit=crop"
            },
            {
                "name": "Florence",
                "country": "Italy",
                "description": "Renaissance art, Uffizi Gallery, Italian heritage",
                "price": "₹32K",
                "hotel": "₹10,000/night",
                "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=250&fit=crop"
            },
            {
                "name": "Jaipur",
                "country": "India",
                "description": "Pink City with palaces, forts, and Rajasthani culture",
                "price": "₹6K",
                "hotel": "₹3,000/night",
                "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=250&fit=crop"
            },
            {
                "name": "Istanbul",
                "country": "Turkey",
                "description": "Where East meets West, rich Ottoman and Byzantine heritage",
                "price": "₹25K",
                "hotel": "₹8,000/night",
                "image": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=400&h=250&fit=crop"
            },
            {
                "name": "Vienna",
                "country": "Austria",
                "description": "Classical music, opera, imperial palaces",
                "price": "₹38K",
                "hotel": "₹11,000/night",
                "image": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(cultural_destinations)

    
    # NATURE DESTINATIONS
    with interest_tabs[2]:
        st.markdown("### 🌳 Best Nature & Wildlife Destinations")
        st.markdown("*Explore national parks, wildlife safaris, and pristine natural beauty*")
        
        nature_destinations = [
            {
                "name": "Amazon Rainforest",
                "country": "Brazil",
                "description": "World's largest rainforest, incredible biodiversity",
                "price": "₹55K",
                "hotel": "₹8,000/night",
                "image": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=400&h=250&fit=crop"
            },
            {
                "name": "Serengeti",
                "country": "Tanzania",
                "description": "Epic wildlife safaris, Great Migration, Big Five",
                "price": "₹80K",
                "hotel": "₹25,000/night",
                "image": "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=400&h=250&fit=crop"
            },
            {
                "name": "Banff National Park",
                "country": "Canada",
                "description": "Stunning Rocky Mountains, turquoise lakes, glaciers",
                "price": "₹50K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1503614472-8c93d56e92ce?w=400&h=250&fit=crop"
            },
            {
                "name": "Kruger National Park",
                "country": "South Africa",
                "description": "Premier safari destination, Big Five wildlife",
                "price": "₹45K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=400&h=250&fit=crop"
            },
            {
                "name": "Galápagos Islands",
                "country": "Ecuador",
                "description": "Unique wildlife, Darwin's inspiration, pristine nature",
                "price": "₹90K",
                "hotel": "₹20,000/night",
                "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=250&fit=crop"
            },
            {
                "name": "Jim Corbett",
                "country": "India",
                "description": "India's oldest national park, Bengal tigers, elephants",
                "price": "₹12K",
                "hotel": "₹5,000/night",
                "image": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(nature_destinations)

    
    # FOOD DESTINATIONS
    with interest_tabs[3]:
        st.markdown("### 🍕 Best Food & Culinary Destinations")
        st.markdown("*Savor world-class cuisine, street food, and gastronomic experiences*")
        
        food_destinations = [
            {
                "name": "Tokyo",
                "country": "Japan",
                "description": "Most Michelin stars, sushi, ramen, street food paradise",
                "price": "₹26K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=250&fit=crop"
            },
            {
                "name": "Bangkok",
                "country": "Thailand",
                "description": "Street food capital, pad thai, tom yum, night markets",
                "price": "₹16K",
                "hotel": "₹5,200/night",
                "image": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&h=250&fit=crop"
            },
            {
                "name": "Bologna",
                "country": "Italy",
                "description": "Food capital of Italy, pasta, prosciutto, authentic cuisine",
                "price": "₹30K",
                "hotel": "₹9,000/night",
                "image": "images/bologna.png"
            },
            {
                "name": "Mumbai",
                "country": "India",
                "description": "Street food haven, vada pav, pav bhaji, diverse cuisine",
                "price": "₹5K",
                "hotel": "₹3,500/night",
                "image": "https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=400&h=250&fit=crop"
            },
            {
                "name": "Lyon",
                "country": "France",
                "description": "Gastronomic capital, bouchons, French fine dining",
                "price": "₹35K",
                "hotel": "₹11,000/night",
                "image": "https://images.unsplash.com/photo-1524396309943-e03f5249f002?w=400&h=250&fit=crop"
            },
            {
                "name": "Singapore",
                "country": "Singapore",
                "description": "Hawker centers, chili crab, laksa, fusion cuisine",
                "price": "₹25K",
                "hotel": "₹4,000/night",
                "image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(food_destinations)
    
    # FESTIVALS DESTINATIONS
    with interest_tabs[4]:
        st.markdown("### 🎉 Best Festival Destinations")
        st.markdown("*Experience vibrant celebrations, cultural events, and world-famous festivals*")
        
        festival_destinations = [
            {
                "name": "Rio de Janeiro",
                "country": "Brazil",
                "description": "Carnival capital, samba parades, world's biggest party",
                "price": "₹65K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=400&h=250&fit=crop"
            },
            {
                "name": "Munich",
                "country": "Germany",
                "description": "Oktoberfest, beer gardens, Bavarian culture",
                "price": "₹40K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1595867818082-083862f3d630?w=400&h=250&fit=crop"
            },
            {
                "name": "Jaipur",
                "country": "India",
                "description": "Holi festival, Diwali celebrations, colorful traditions",
                "price": "₹6K",
                "hotel": "₹3,000/night",
                "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=250&fit=crop"
            },
            {
                "name": "Edinburgh",
                "country": "Scotland",
                "description": "Fringe Festival, Hogmanay, cultural celebrations",
                "price": "₹45K",
                "hotel": "₹14,000/night",
                "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=400&h=250&fit=crop"
            },
            {
                "name": "Chiang Mai",
                "country": "Thailand",
                "description": "Yi Peng Lantern Festival, Songkran water festival",
                "price": "₹18K",
                "hotel": "₹4,500/night",
                "image": "https://images.unsplash.com/photo-1598970434795-0c54fe7c0648?w=400&h=250&fit=crop"
            },
            {
                "name": "New Orleans",
                "country": "USA",
                "description": "Mardi Gras, jazz festivals, vibrant celebrations",
                "price": "₹55K",
                "hotel": "₹16,000/night",
                "image": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(festival_destinations)

    
    # HISTORICAL DESTINATIONS
    with interest_tabs[5]:
        st.markdown("### 🏛️ Best Historical Destinations")
        st.markdown("*Explore ancient ruins, UNESCO sites, and historical landmarks*")
        
        historical_destinations = [
            {
                "name": "Rome",
                "country": "Italy",
                "description": "Colosseum, Roman Forum, Vatican, ancient history",
                "price": "₹35K",
                "hotel": "₹11,000/night",
                "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=250&fit=crop"
            },
            {
                "name": "Athens",
                "country": "Greece",
                "description": "Acropolis, Parthenon, birthplace of democracy",
                "price": "₹32K",
                "hotel": "₹9,000/night",
                "image": "https://images.unsplash.com/photo-1555993539-1732b0258235?w=400&h=250&fit=crop"
            },
            {
                "name": "Cairo",
                "country": "Egypt",
                "description": "Pyramids of Giza, Sphinx, ancient Egyptian civilization",
                "price": "₹28K",
                "hotel": "₹8,000/night",
                "image": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=400&h=250&fit=crop"
            },
            {
                "name": "Agra",
                "country": "India",
                "description": "Taj Mahal, Agra Fort, Mughal architecture",
                "price": "₹4K",
                "hotel": "₹2,500/night",
                "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=400&h=250&fit=crop"
            },
            {
                "name": "Machu Picchu",
                "country": "Peru",
                "description": "Incan citadel, ancient ruins, mountain sanctuary",
                "price": "₹75K",
                "hotel": "₹20,000/night",
                "image": "https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=400&h=250&fit=crop"
            },
            {
                "name": "Petra",
                "country": "Jordan",
                "description": "Rose city, ancient Nabataean capital, carved temples",
                "price": "₹50K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1578895101408-1a36b834405b?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(historical_destinations)

    
    # SHOPPING DESTINATIONS
    with interest_tabs[6]:
        st.markdown("### 🛍️ Best Shopping Destinations")
        st.markdown("*Luxury malls, street markets, fashion districts, and shopping paradise*")
        
        shopping_destinations = [
            {
                "name": "Dubai",
                "country": "UAE",
                "description": "Dubai Mall, Gold Souk, luxury shopping, tax-free",
                "price": "₹17K",
                "hotel": "₹5,000/night",
                "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"
            },
            {
                "name": "Hong Kong",
                "country": "China",
                "description": "Shopping paradise, street markets, luxury brands",
                "price": "₹24K",
                "hotel": "₹10,000/night",
                "image": "https://images.unsplash.com/photo-1536599018102-9f803c140fc1?w=400&h=250&fit=crop"
            },
            {
                "name": "Milan",
                "country": "Italy",
                "description": "Fashion capital, designer boutiques, Galleria Vittorio",
                "price": "₹38K",
                "hotel": "₹13,000/night",
                "image": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd?w=400&h=250&fit=crop"
            },
            {
                "name": "Bangkok",
                "country": "Thailand",
                "description": "Chatuchak Market, night bazaars, affordable shopping",
                "price": "₹16K",
                "hotel": "₹5,200/night",
                "image": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&h=250&fit=crop"
            },
            {
                "name": "New York",
                "country": "USA",
                "description": "Fifth Avenue, SoHo, Times Square, flagship stores",
                "price": "₹60K",
                "hotel": "₹20,000/night",
                "image": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400&h=250&fit=crop"
            },
            {
                "name": "Istanbul",
                "country": "Turkey",
                "description": "Grand Bazaar, spice markets, Turkish carpets",
                "price": "₹25K",
                "hotel": "₹8,000/night",
                "image": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(shopping_destinations)

    
    # BEACHES DESTINATIONS
    with interest_tabs[7]:
        st.markdown("### 🏖️ Best Beach Destinations")
        st.markdown("*Crystal clear waters, white sand beaches, tropical paradise*")
        
        beach_destinations = [
            {
                "name": "Maldives",
                "country": "Maldives",
                "description": "Overwater bungalows, coral reefs, pristine beaches",
                "price": "₹45K",
                "hotel": "₹25,000/night",
                "image": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400&h=250&fit=crop"
            },
            {
                "name": "Bali",
                "country": "Indonesia",
                "description": "Tropical paradise, surf beaches, beach clubs",
                "price": "₹20K",
                "hotel": "₹6,000/night",
                "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop"
            },
            {
                "name": "Phuket",
                "country": "Thailand",
                "description": "Patong Beach, island hopping, water sports",
                "price": "₹28K",
                "hotel": "₹10,000/night",
                "image": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=400&h=250&fit=crop"
            },
            {
                "name": "Goa",
                "country": "India",
                "description": "Beach parties, Portuguese heritage, coastal beauty",
                "price": "₹8K",
                "hotel": "₹4,000/night",
                "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400&h=250&fit=crop"
            },
            {
                "name": "Santorini",
                "country": "Greece",
                "description": "Black sand beaches, cliff views, sunset paradise",
                "price": "₹50K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=400&h=250&fit=crop"
            },
            {
                "name": "Cancun",
                "country": "Mexico",
                "description": "Caribbean beaches, Mayan ruins, resort paradise",
                "price": "₹65K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1568402102990-bc541580b59f?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(beach_destinations)

    
    # MOUNTAINS DESTINATIONS
    with interest_tabs[8]:
        st.markdown("### ⛰️ Best Mountain Destinations")
        st.markdown("*Majestic peaks, alpine villages, skiing, and mountain adventures*")
        
        mountain_destinations = [
            {
                "name": "Swiss Alps",
                "country": "Switzerland",
                "description": "Matterhorn, skiing, alpine villages, scenic trains",
                "price": "₹55K",
                "hotel": "₹20,000/night",
                "image": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=400&h=250&fit=crop"
            },
            {
                "name": "Manali",
                "country": "India",
                "description": "Himalayan paradise, Rohtang Pass, adventure sports",
                "price": "₹10K",
                "hotel": "₹3,500/night",
                "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=250&fit=crop"
            },
            {
                "name": "Queenstown",
                "country": "New Zealand",
                "description": "Adventure capital, Remarkables range, skiing",
                "price": "₹70K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=400&h=250&fit=crop"
            },
            {
                "name": "Banff",
                "country": "Canada",
                "description": "Rocky Mountains, Lake Louise, wilderness",
                "price": "₹50K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1503614472-8c93d56e92ce?w=400&h=250&fit=crop"
            },
            {
                "name": "Chamonix",
                "country": "France",
                "description": "Mont Blanc, skiing, mountaineering paradise",
                "price": "₹48K",
                "hotel": "₹16,000/night",
                "image": "https://images.unsplash.com/photo-1605540436563-5bca919ae766?w=400&h=250&fit=crop"
            },
            {
                "name": "Leh-Ladakh",
                "country": "India",
                "description": "High altitude desert, monasteries, mountain passes",
                "price": "₹15K",
                "hotel": "₹4,000/night",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(mountain_destinations)

    
    # OUTDOORS DESTINATIONS
    with interest_tabs[9]:
        st.markdown("### 🏕️ Best Outdoor Adventure Destinations")
        st.markdown("*Hiking, camping, trekking, and wilderness experiences*")
        
        outdoor_destinations = [
            {
                "name": "Patagonia",
                "country": "Argentina/Chile",
                "description": "Glaciers, trekking, Torres del Paine, wilderness",
                "price": "₹85K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400&h=250&fit=crop"
            },
            {
                "name": "Iceland",
                "country": "Iceland",
                "description": "Waterfalls, geysers, Northern Lights, hiking",
                "price": "₹60K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1504829857797-ddff29c27927?w=400&h=250&fit=crop"
            },
            {
                "name": "Rishikesh",
                "country": "India",
                "description": "River rafting, bungee jumping, yoga, camping",
                "price": "₹7K",
                "hotel": "₹2,500/night",
                "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=250&fit=crop"
            },
            {
                "name": "Yosemite",
                "country": "USA",
                "description": "Rock climbing, hiking, waterfalls, camping",
                "price": "₹58K",
                "hotel": "₹14,000/night",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop"
            },
            {
                "name": "Nepal",
                "country": "Nepal",
                "description": "Everest Base Camp, trekking, mountain adventures",
                "price": "₹22K",
                "hotel": "₹3,000/night",
                "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=400&h=250&fit=crop"
            },
            {
                "name": "New Zealand",
                "country": "New Zealand",
                "description": "Milford Track, adventure sports, scenic hikes",
                "price": "₹70K",
                "hotel": "₹16,000/night",
                "image": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(outdoor_destinations)

    
    # NIGHTLIFE DESTINATIONS
    with interest_tabs[10]:
        st.markdown("### 🎊 Best Nightlife Destinations")
        st.markdown("*Clubs, bars, parties, and vibrant nightlife scenes*")
        
        nightlife_destinations = [
            {
                "name": "Ibiza",
                "country": "Spain",
                "description": "Party island, world-class DJs, beach clubs",
                "price": "₹42K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400&h=250&fit=crop"
            },
            {
                "name": "Las Vegas",
                "country": "USA",
                "description": "Casino capital, nightclubs, entertainment shows",
                "price": "₹52K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1605833556294-ea5c7a74f57d?w=400&h=250&fit=crop"
            },
            {
                "name": "Berlin",
                "country": "Germany",
                "description": "Techno clubs, underground scene, 24/7 parties",
                "price": "₹38K",
                "hotel": "₹10,000/night",
                "image": "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=400&h=250&fit=crop"
            },
            {
                "name": "Bangkok",
                "country": "Thailand",
                "description": "Rooftop bars, night markets, Khao San Road",
                "price": "₹16K",
                "hotel": "₹5,200/night",
                "image": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&h=250&fit=crop"
            },
            {
                "name": "Miami",
                "country": "USA",
                "description": "South Beach, clubs, Latin vibes, beach parties",
                "price": "₹55K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1533106418989-88406c7cc8ca?w=400&h=250&fit=crop"
            },
            {
                "name": "Amsterdam",
                "country": "Netherlands",
                "description": "Red light district, canal parties, vibrant bars",
                "price": "₹40K",
                "hotel": "₹13,000/night",
                "image": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(nightlife_destinations)

    
    # LUXURY DESTINATIONS
    with interest_tabs[11]:
        st.markdown("### 💎 Best Luxury Destinations")
        st.markdown("*5-star resorts, exclusive experiences, premium travel*")
        
        luxury_destinations = [
            {
                "name": "Monaco",
                "country": "Monaco",
                "description": "Casinos, yachts, F1 Grand Prix, luxury lifestyle",
                "price": "₹80K",
                "hotel": "₹35,000/night",
                "image": "images/monaco.png"
            },
            {
                "name": "Dubai",
                "country": "UAE",
                "description": "Burj Al Arab, luxury malls, desert safaris",
                "price": "₹17K",
                "hotel": "₹5,000/night",
                "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"
            },
            {
                "name": "Maldives",
                "country": "Maldives",
                "description": "Private islands, overwater villas, spa resorts",
                "price": "₹45K",
                "hotel": "₹25,000/night",
                "image": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400&h=250&fit=crop"
            },
            {
                "name": "Paris",
                "country": "France",
                "description": "Luxury hotels, Michelin dining, haute couture",
                "price": "₹35K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=250&fit=crop"
            },
            {
                "name": "Bora Bora",
                "country": "French Polynesia",
                "description": "Exclusive resorts, turquoise lagoons, paradise",
                "price": "₹1.2L",
                "hotel": "₹45,000/night",
                "image": "images/borabora.png",
                "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
            },
            {
                "name": "St. Moritz",
                "country": "Switzerland",
                "description": "Luxury ski resort, alpine elegance, winter sports",
                "price": "₹65K",
                "hotel": "₹28,000/night",
                "image": "https://images.unsplash.com/photo-1605540436563-5bca919ae766?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(luxury_destinations)
    
    # WELLNESS DESTINATIONS
    with interest_tabs[12]:
        st.markdown("### 🧘 Best Wellness & Spa Destinations")
        st.markdown("*Yoga retreats, spa resorts, meditation, and rejuvenation*")
        
        wellness_destinations = [
            {
                "name": "Ubud",
                "country": "Bali, Indonesia",
                "description": "Yoga capital, spa retreats, healing centers",
                "price": "₹22K",
                "hotel": "₹7,000/night",
                "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop"
            },
            {
                "name": "Rishikesh",
                "country": "India",
                "description": "Yoga capital of the world, ashrams, Ganges",
                "price": "₹7K",
                "hotel": "₹2,500/night",
                "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=250&fit=crop"
            },
            {
                "name": "Phuket",
                "country": "Thailand",
                "description": "Spa resorts, Thai massage, wellness retreats",
                "price": "₹28K",
                "hotel": "₹10,000/night",
                "image": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=400&h=250&fit=crop"
            },
            {
                "name": "Kerala",
                "country": "India",
                "description": "Ayurveda treatments, backwaters, spa resorts",
                "price": "₹12K",
                "hotel": "₹5,000/night",
                "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400&h=250&fit=crop"
            },
            {
                "name": "Sedona",
                "country": "USA",
                "description": "Spiritual vortexes, spa resorts, meditation",
                "price": "₹55K",
                "hotel": "₹16,000/night",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop"
            },
            {
                "name": "Santorini",
                "country": "Greece",
                "description": "Luxury spas, caldera views, relaxation",
                "price": "₹50K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(wellness_destinations)

    
    # ROMANCE DESTINATIONS
    with interest_tabs[13]:
        st.markdown("### 💑 Best Romantic Destinations")
        st.markdown("*Honeymoon spots, couple getaways, romantic experiences*")
        
        romance_destinations = [
            {
                "name": "Paris",
                "country": "France",
                "description": "City of love, Eiffel Tower, Seine cruises",
                "price": "₹35K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=250&fit=crop"
            },
            {
                "name": "Venice",
                "country": "Italy",
                "description": "Gondola rides, canals, romantic bridges",
                "price": "₹38K",
                "hotel": "₹14,000/night",
                "image": "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=400&h=250&fit=crop"
            },
            {
                "name": "Santorini",
                "country": "Greece",
                "description": "Sunset views, white-washed buildings, wine",
                "price": "₹50K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=400&h=250&fit=crop"
            },
            {
                "name": "Udaipur",
                "country": "India",
                "description": "City of lakes, palaces, romantic boat rides",
                "price": "₹8K",
                "hotel": "₹4,500/night",
                "image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=400&h=250&fit=crop"
            },
            {
                "name": "Maldives",
                "country": "Maldives",
                "description": "Private islands, overwater dinners, seclusion",
                "price": "₹45K",
                "hotel": "₹25,000/night",
                "image": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400&h=250&fit=crop"
            },
            {
                "name": "Prague",
                "country": "Czech Republic",
                "description": "Fairy-tale city, castle views, cobblestone streets",
                "price": "₹32K",
                "hotel": "₹9,000/night",
                "image": "https://images.unsplash.com/photo-1541849546-216549ae216d?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(romance_destinations)

    
    # NIGHT SKIES DESTINATIONS
    with interest_tabs[14]:
        st.markdown("### ✨ Best Night Skies & Stargazing Destinations")
        st.markdown("*Northern Lights, dark sky reserves, astronomical wonders*")
        
        nightsky_destinations = [
            {
                "name": "Iceland",
                "country": "Iceland",
                "description": "Northern Lights, aurora borealis, dark winters",
                "price": "₹60K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1504829857797-ddff29c27927?w=400&h=250&fit=crop"
            },
            {
                "name": "Tromsø",
                "country": "Norway",
                "description": "Arctic aurora, midnight sun, polar nights",
                "price": "₹55K",
                "hotel": "₹16,000/night",
                "image": "https://images.unsplash.com/photo-1579033461380-adb47c3eb938?w=400&h=250&fit=crop"
            },
            {
                "name": "Atacama Desert",
                "country": "Chile",
                "description": "Clearest skies, observatories, Milky Way",
                "price": "₹75K",
                "hotel": "₹14,000/night",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop"
            },
            {
                "name": "Spiti Valley",
                "country": "India",
                "description": "High altitude, clear skies, stargazing camps",
                "price": "₹12K",
                "hotel": "₹3,000/night",
                "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=250&fit=crop"
            },
            {
                "name": "Lapland",
                "country": "Finland",
                "description": "Aurora hunting, glass igloos, winter wonderland",
                "price": "₹58K",
                "hotel": "₹20,000/night",
                "image": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=400&h=250&fit=crop"
            },
            {
                "name": "Mauna Kea",
                "country": "Hawaii, USA",
                "description": "World-class observatories, volcanic summit",
                "price": "₹65K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1542259009477-d625272157b7?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(nightsky_destinations)

    
    # SPORTS DESTINATIONS
    with interest_tabs[15]:
        st.markdown("### ⚽ Best Sports & Adventure Destinations")
        st.markdown("*Extreme sports, adventure activities, sporting events*")
        
        sports_destinations = [
            {
                "name": "Queenstown",
                "country": "New Zealand",
                "description": "Bungee jumping, skydiving, adventure capital",
                "price": "₹70K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=400&h=250&fit=crop"
            },
            {
                "name": "Interlaken",
                "country": "Switzerland",
                "description": "Paragliding, skiing, canyoning, skydiving",
                "price": "₹52K",
                "hotel": "₹17,000/night",
                "image": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=400&h=250&fit=crop"
            },
            {
                "name": "Whistler",
                "country": "Canada",
                "description": "Skiing, snowboarding, mountain biking",
                "price": "₹55K",
                "hotel": "₹16,000/night",
                "image": "https://images.unsplash.com/photo-1605540436563-5bca919ae766?w=400&h=250&fit=crop"
            },
            {
                "name": "Goa",
                "country": "India",
                "description": "Water sports, parasailing, jet skiing, diving",
                "price": "₹8K",
                "hotel": "₹4,000/night",
                "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400&h=250&fit=crop"
            },
            {
                "name": "Dubai",
                "country": "UAE",
                "description": "Desert safari, skydiving, indoor skiing",
                "price": "₹17K",
                "hotel": "₹5,000/night",
                "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"
            },
            {
                "name": "Costa Rica",
                "country": "Costa Rica",
                "description": "Surfing, zip-lining, white water rafting",
                "price": "₹68K",
                "hotel": "₹12,000/night",
                "image": "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(sports_destinations)

    
    # OFFBEAT DESTINATIONS
    with interest_tabs[16]:
        st.markdown("### 🌟 Best Offbeat & Unique Destinations")
        st.markdown("*Hidden gems, unexplored places, unique experiences*")
        
        offbeat_destinations = [
            {
                "name": "Faroe Islands",
                "country": "Denmark",
                "description": "Remote islands, dramatic cliffs, untouched nature",
                "price": "₹62K",
                "hotel": "₹15,000/night",
                "image": "https://images.unsplash.com/photo-1551244072-5d12893278ab?w=400&h=250&fit=crop"
            },
            {
                "name": "Bhutan",
                "country": "Bhutan",
                "description": "Happiness kingdom, monasteries, pristine culture",
                "price": "₹35K",
                "hotel": "₹8,000/night",
                "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400&h=250&fit=crop"
            },
            {
                "name": "Socotra",
                "country": "Yemen",
                "description": "Alien landscape, dragon blood trees, unique flora",
                "price": "₹85K",
                "hotel": "₹10,000/night",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop"
            },
            {
                "name": "Meghalaya",
                "country": "India",
                "description": "Living root bridges, wettest place, tribal culture",
                "price": "₹10K",
                "hotel": "₹3,500/night",
                "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=250&fit=crop"
            },
            {
                "name": "Madagascar",
                "country": "Madagascar",
                "description": "Unique wildlife, baobab trees, lemurs",
                "price": "₹72K",
                "hotel": "₹11,000/night",
                "image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=400&h=250&fit=crop"
            },
            {
                "name": "Svalbard",
                "country": "Norway",
                "description": "Arctic wilderness, polar bears, northernmost town",
                "price": "₹78K",
                "hotel": "₹18,000/night",
                "image": "https://images.unsplash.com/photo-1579033461380-adb47c3eb938?w=400&h=250&fit=crop"
            },
        ]
        
        render_destination_cards(offbeat_destinations)


# ============================================================================
# TAB 3: FLIGHTS
# ============================================================================
with tab3:
    st.header("✈️ Flight Search & Booking")
    
    # Search Form
    st.markdown("### 🔍 Search Flights with AI")
    
    # City Data
    flight_cities = [
        "Delhi, India", "Mumbai, India", "Bangalore, India", "Chennai, India", "Kolkata, India", "Hyderabad, India", 
        "Pune, India", "Goa, India", "Jaipur, India", "Ahmedabad, India", "Cochin, India",
        "Dubai, UAE", "Bangkok, Thailand", "Singapore", "London, UK", "New York, USA", "Paris, France", 
        "Tokyo, Japan", "Bali, Indonesia", "Phuket, Thailand", "Kuala Lumpur, Malaysia", 
        "Sydney, Australia", "Toronto, Canada", "Frankfurt, Germany", "Amsterdam, Netherlands"
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        flight_from = st.selectbox("✈️ From (City/Airport)", ["Select City"] + flight_cities, index=1, key="flight_from")
    with col2:
        flight_to = st.selectbox("🛬 To (City/Airport)", ["Select City"] + flight_cities, index=11, key="flight_to")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        flight_date = st.date_input("📅 Departure", key="flight_date")
    with col4:
        flight_class = st.selectbox("🎫 Class", ["Economy", "Premium Economy", "Business", "First"], key="flight_class")
    with col5:
        passenger_count = st.number_input("👥 Passengers", min_value=1, value=1, key="flight_passengers")
        
    if st.button("🔍 Search Flights with AI", use_container_width=True):
        if flight_from and flight_to:
            details = f"Class: {flight_class}, Passengers: {passenger_count}"
            st.info(f"Searching flights from {flight_from} to {flight_to}...")
            result = run_booking_crew("Flights", flight_from, flight_to, flight_date, details)
            st.code(result, language="markdown")
            
            # Save to History
            history_dir = "Flight_Search_History"
            if not os.path.exists(history_dir): os.makedirs(history_dir)
            filename = f"Flight_Options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(history_dir, filename)
            
            # Save with Metadata Header for easier history parsing
            file_content = f"DETAILS\nFrom: {flight_from}\nTo: {flight_to}\nDate: {flight_date}\n---\n{result}"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(file_content)
            
            st.download_button(
                label="📥 Download Flight Options",
                data=file_content,
                file_name=filename,
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please enter departure and arrival locations.")
    
    st.markdown("---")
    
    # Popular Routes
    st.markdown("### 🔥 Popular Flight Routes from India")
    
    popular_routes = [
        {"route": "Delhi → Dubai", "price": "₹12,500", "duration": "3h 30m", "airline": "Emirates"},
        {"route": "Mumbai → Singapore", "price": "₹18,900", "duration": "5h 45m", "airline": "Singapore Airlines"},
        {"route": "Bangalore → Bangkok", "price": "₹14,200", "duration": "3h 50m", "airline": "Thai Airways"},
        {"route": "Delhi → London", "price": "₹42,000", "duration": "9h 15m", "airline": "British Airways"},
        {"route": "Mumbai → New York", "price": "₹65,000", "duration": "15h 30m", "airline": "Air India"},
        {"route": "Chennai → Kuala Lumpur", "price": "₹11,800", "duration": "4h 10m", "airline": "AirAsia"},
    ]
    
    cols = st.columns(2)
    for idx, route in enumerate(popular_routes):
        with cols[idx % 2]:
            st.markdown(
                f'<div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">'
                f'<h4 style="margin: 0 0 10px 0; color: white;">&#9992; {route["route"]}</h4>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#128176; From:</strong> {route["price"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#9201; Duration:</strong> {route["duration"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#128747; Airline:</strong> {route["airline"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    st.markdown("---")
    st.info("🛈 **Coming Soon:** Real-time flight booking integration with multiple airlines!")

# TAB 3 HISTORY
with tab3_hist:
    render_history_tab("Flight_Search_History", "Flight")

# ============================================================================
# TAB 4: HOTELS
# ============================================================================
with tab4:
    st.header("🏨 Hotel Search & Booking")
    
    # Search Form
    st.markdown("### 🔍 Find Hotels with AI")
    
    # Hotel Cities
    hotel_cities = [
        "Goa, India", "Jaipur, India", "Manali, India", "Kerala, India", "Udaipur, India",
        "Bangkok, Thailand", "Dubai, UAE", "Bali, Indonesia", "Maldives",
        "Singapore", "Paris, France", "London, UK", "New York, USA", "Tokyo, Japan",
        "Switzerland", "Italy", "Santorini, Greece"
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        hotel_city = st.selectbox("📍 Destination City", ["Select City"] + hotel_cities, index=1, key="hotel_city")
    with col2:
        hotel_guests = st.number_input("👥 Guests", min_value=1, max_value=10, value=2, key="hotel_guests")
    
    col3, col4 = st.columns(2)
    with col3:
        checkin = st.date_input("📅 Check-in", key="hotel_checkin")
    with col4:
        checkout = st.date_input("📅 Check-out", key="hotel_checkout")
    
    col5, col6 = st.columns(2)
    with col5:
        hotel_type = st.selectbox("🏨 Type", ["All", "5-Star", "4-Star", "3-Star", "Budget", "Boutique"], key="hotel_type")
    with col6:
        price_range = st.select_slider("💰 Price Range", options=["Budget", "Mid-Range", "Luxury", "Ultra-Luxury"], key="hotel_price")
    
    if st.button("🔍 Search Hotels with AI", use_container_width=True):
        if hotel_city:
            details = f"Guests: {hotel_guests}, Check-in: {checkin}, Check-out: {checkout}, Type: {hotel_type}, Price: {price_range}"
            st.info(f"Searching hotels in {hotel_city}...")
            result = run_booking_crew("Hotels", "N/A", hotel_city, checkin, details)
            st.code(result, language="markdown")
            
            # Save to History
            history_dir = "Hotel_Search_History"
            if not os.path.exists(history_dir): os.makedirs(history_dir)
            filename = f"Hotel_Options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(history_dir, filename)
            
            # Save with Metadata Header
            file_content = f"DETAILS\nFrom: N/A\nTo: {hotel_city}\nDate: {checkin}\n---\n{result}"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(file_content)
                
            st.download_button(
                label="📥 Download Hotel Options",
                data=file_content,
                file_name=filename,
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please enter a destination city.")
    
    st.markdown("---")
    
    # Featured Hotels
    st.markdown("### ⭐ Featured Hotels")
    
    featured_hotels = [
        {"name": "Burj Al Arab", "city": "Dubai", "rating": "5⭐", "price": "₹45,000/night", "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"},
        {"name": "Marina Bay Sands", "city": "Singapore", "rating": "5⭐", "price": "₹28,000/night", "image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=400&h=250&fit=crop"},
        {"name": "The Ritz Paris", "city": "Paris", "rating": "5⭐", "price": "₹55,000/night", "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=250&fit=crop"},
        {"name": "Park Hyatt Tokyo", "city": "Tokyo", "rating": "5⭐", "price": "₹32,000/night", "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=250&fit=crop"},
        {"name": "Anantara Bali", "city": "Bali", "rating": "5⭐", "price": "₹18,000/night", "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop"},
        {"name": "Mandarin Oriental", "city": "Bangkok", "rating": "5⭐", "price": "₹22,000/night", "image": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&h=250&fit=crop"},
    ]
    
    cols = st.columns(3)
    for idx, hotel in enumerate(featured_hotels):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="destination-card">'
                f'<img src="{hotel["image"]}" style="width: 100%; height: 180px; object-fit: cover;" alt="{hotel["name"]}">'
                f'<div style="padding: 15px;">'
                f'<h4 style="margin: 0 0 5px 0; color: #1a1a1a;">{hotel["name"]}</h4>'
                f'<p style="margin: 5px 0; color: #666;">&#128205; {hotel["city"]}</p>'
                f'<p style="margin: 5px 0; color: #ff6b6b;"><strong>{hotel["rating"]}</strong></p>'
                f'<p style="margin: 5px 0; color: #4ecdc4;"><strong>{hotel["price"]}</strong></p>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    st.info("🛈 **Coming Soon:** Direct hotel booking with best price guarantee!")
    
# TAB 4 HISTORY
with tab4_hist:
    render_history_tab("Hotel_Search_History", "Hotel")

# ============================================================================
# TAB 5: TRAINS
# ============================================================================
with tab5:
    st.header("🚂 Train Booking")
    
    # Search Form
    st.markdown("### 🔍 Search Trains with AI")
    
    # Train Stations
    train_stations = [
        "New Delhi (NDLS)", "Mumbai Central (MMCT)", "Howrah Jn (HWH)", "Chennai Central (MAS)", 
        "Bangalore City (SBC)", "Secunderabad (SC)", "Pune Jn (PUNE)", "Ahmedabad (ADI)", 
        "Jaipur (JP)", "Varanasi (BSB)", "Agra Cantt (AGC)", "Goa (Madgaon)"
    ]

    col1, col2 = st.columns(2)
    with col1:
        train_from = st.selectbox("🚉 From Station", ["Select Station"] + train_stations, index=1, key="train_from")
    with col2:
        train_to = st.selectbox("🚉 To Station", ["Select Station"] + train_stations, index=10, key="train_to")
    
    col3, col4 = st.columns(2)
    with col3:
        train_date = st.date_input("📅 Journey Date", key="train_date")
    with col4:
        train_class = st.selectbox("🎫 Class", ["All Classes", "AC 1st", "AC 2-Tier", "AC 3-Tier", "Sleeper"], key="train_class")
    
    if st.button("🔍 Search Trains with AI", use_container_width=True):
        if train_from and train_to:
            details = f"Class: {train_class}"
            st.info(f"Searching trains from {train_from} to {train_to}...")
            result = run_booking_crew("Trains", train_from, train_to, train_date, details)
            st.code(result, language="markdown")
            
            # Save to History
            history_dir = "Train_Search_History"
            if not os.path.exists(history_dir): os.makedirs(history_dir)
            filename = f"Train_Options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(history_dir, filename)
            
            # Save with Metadata Header
            file_content = f"DETAILS\nFrom: {train_from}\nTo: {train_to}\nDate: {train_date}\n---\n{result}"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(file_content)
                
            st.download_button(
                label="📥 Download Train Options",
                data=file_content,
                file_name=filename,
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please enter departure and arrival stations.")
    
    st.markdown("---")
    
    # Popular Train Routes
    st.markdown("### 🚄 Popular Train Routes")
    
    train_routes = [
        {"train": "Rajdhani Express", "route": "Delhi → Mumbai", "duration": "15h 50m", "price": "₹2,500"},
        {"train": "Shatabdi Express", "route": "Delhi → Agra", "duration": "2h 10m", "price": "₹750"},
        {"train": "Duronto Express", "route": "Mumbai → Goa", "duration": "11h 30m", "price": "₹1,800"},
        {"train": "Gatimaan Express", "route": "Delhi → Jaipur", "duration": "4h 25m", "price": "₹1,200"},
        {"train": "Vande Bharat", "route": "Delhi → Varanasi", "duration": "8h 00m", "price": "₹1,950"},
        {"train": "Tejas Express", "route": "Mumbai → Goa", "duration": "8h 45m", "price": "₹1,650"},
    ]
    
    cols = st.columns(2)
    for idx, train in enumerate(train_routes):
        with cols[idx % 2]:
            st.markdown(
                f'<div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 15px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">'
                f'<h4 style="margin: 0 0 10px 0; color: white;">&#128642; {train["train"]}</h4>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#128205; Route:</strong> {train["route"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#9201; Duration:</strong> {train["duration"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#128176; From:</strong> {train["price"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # PNR Status Checker
    st.markdown("### 🔍 PNR Status")
    pnr_number = st.text_input("Enter 10-digit PNR Number")
    if st.button("Check Status"):
        if pnr_number:
            st.info("🔄 Checking PNR status...")
        else:
            st.warning("⚠️ Please enter a valid PNR number")

# TAB 5 HISTORY
with tab5_hist:
    render_history_tab("Train_Search_History", "Train")

# ============================================================================
# TAB 6: BUSES
# ============================================================================
with tab6:
    st.header("🚌 Bus Booking")
    
    # Search Form
    st.markdown("### 🔍 Search Buses with AI")
    
    # Bus Cities
    bus_cities = [
        "Delhi", "Manali", "Shimla", "Jaipur", "Agra", "Haridwar", "Rishikesh", "Dehradun",
        "Mumbai", "Pune", "Goa", "Lonavala", "Mahabaleshwar", "Nashik", "Shirdi",
        "Bangalore", "Mysore", "Coorg", "Ooty", "Chennai", "Pondicherry", "Hyderabad", "Tirupati"
    ]

    col1, col2 = st.columns(2)
    with col1:
        bus_from = st.selectbox("🚏 From City", ["Select City"] + bus_cities, index=1, key="bus_from")
    with col2:
        bus_to = st.selectbox("🚏 To City", ["Select City"] + bus_cities, index=5, key="bus_to")
    
    col3, col4 = st.columns(2)
    with col3:
        bus_date = st.date_input("📅 Travel Date", key="bus_date")
    with col4:
        bus_type = st.selectbox("🚌 Bus Type", ["All", "AC Sleeper", "AC Seater", "Non-AC Sleeper", "Volvo"], key="bus_type")
    
    if st.button("🔍 Search Buses with AI", use_container_width=True):
        if bus_from and bus_to:
            details = f"Type: {bus_type}"
            st.info(f"Searching buses from {bus_from} to {bus_to}...")
            result = run_booking_crew("Buses", bus_from, bus_to, bus_date, details)
            st.code(result, language="markdown")
            
            # Save to History
            history_dir = "Bus_Search_History"
            if not os.path.exists(history_dir): os.makedirs(history_dir)
            filename = f"Bus_Options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(history_dir, filename)
            
            # Save with Metadata Header
            file_content = f"DETAILS\nFrom: {bus_from}\nTo: {bus_to}\nDate: {bus_date}\n---\n{result}"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(file_content)
                
            st.download_button(
                label="📥 Download Bus Options",
                data=file_content,
                file_name=filename,
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please enter departure and arrival cities.")
    
    st.markdown("---")
    
    # Popular Bus Routes
    st.markdown("### 🚍 Popular Bus Routes")
    
    bus_routes = [
        {"operator": "IntrCity SmartBus", "route": "Delhi → Manali", "duration": "12h 30m", "price": "₹1,200", "type": "AC Sleeper"},
        {"operator": "VRL Travels", "route": "Bangalore → Goa", "duration": "10h 45m", "price": "₹950", "type": "Volvo AC"},
        {"operator": "RedBus Premium", "route": "Mumbai → Pune", "duration": "3h 30m", "price": "₹450", "type": "AC Seater"},
        {"operator": "Parveen Travels", "route": "Delhi → Jaipur", "duration": "5h 15m", "price": "₹650", "type": "AC Sleeper"},
        {"operator": "SRS Travels", "route": "Bangalore → Chennai", "duration": "7h 00m", "price": "₹800", "type": "Volvo AC"},
        {"operator": "Orange Travels", "route": "Hyderabad → Bangalore", "duration": "9h 30m", "price": "₹1,100", "type": "AC Sleeper"},
    ]
    
    cols = st.columns(2)
    for idx, bus in enumerate(bus_routes):
        with cols[idx % 2]:
            st.markdown(
                f'<div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 15px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">'
                f'<h4 style="margin: 0 0 10px 0; color: white;">&#128652; {bus["operator"]}</h4>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#128205; Route:</strong> {bus["route"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#9201; Duration:</strong> {bus["duration"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#127915; Type:</strong> {bus["type"]}</p>'
                f'<p style="margin: 5px 0; color: #f0f0f0;"><strong>&#128176; From:</strong> {bus["price"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    st.info("🛈 **Coming Soon:** Live seat selection and instant booking!")

# TAB 6 HISTORY
with tab6_hist:
    render_history_tab("Bus_Search_History", "Bus")

# ============================================================================
# TAB 7: POPULAR DESTINATIONS
# ============================================================================
with tab7:
    st.header("🌟 Discover Popular Destinations")
    
    st.markdown("### 🔍 Smart Destination Finder")
    
    # Enhanced Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trip_type = st.selectbox("🌍 Trip Type", ["All", "International", "Domestic", "Visa-free"])
    
    with col2:
        weather_pref = st.selectbox("🌤️ Weather", ["All", "No Rain", "Rain", "Snow", "Colder", "Warmer"])
    
    with col3:
        duration = st.selectbox("✈️ Flight Duration", ["All", "< 3hr", "3-6hr", "6-12hr", "12hr+"])
    
    with col4:
        budget = st.selectbox("💰 Budget", ["All", "Budget", "Mid-Range", "Luxury"])
    
    # Interest filters
    st.markdown("### 🎨 Filter by Your Interests")
    interest_filters = st.multiselect(
        "What are you looking for?",
        ["Religious", "Cultural", "Nature", "Food", "Festivals", "Historical", 
         "Shopping", "Beaches", "Mountains", "Outdoors", "Nightlife", "Luxury",
         "Wellness", "Romance", "Sports", "Offbeat"],
        default=["Cultural", "Food"]
    )
    
    st.markdown("---")
    
    # Trending Destinations
    st.markdown("### 🔥 Trending Destinations This Month")
    
    trending_destinations = [
        {"name": "Bangkok", "country": "Thailand", "price": "₹16K", "hotel": "₹5,200/night", "image": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&h=250&fit=crop", "tag": "&#128293; Hot Deal"},
        {"name": "Dubai", "country": "UAE", "price": "₹17K", "hotel": "₹5,000/night", "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop", "tag": "&#10024; Luxury"},
        {"name": "Singapore", "country": "Singapore", "price": "₹25K", "hotel": "₹4,000/night", "image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=400&h=250&fit=crop", "tag": "&#127750; City Break"},
        {"name": "Tokyo", "country": "Japan", "price": "₹26K", "hotel": "₹15,000/night", "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=250&fit=crop", "tag": "&#127884; Cultural"},
        {"name": "Paris", "country": "France", "price": "₹35K", "hotel": "₹12,000/night", "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=250&fit=crop", "tag": "&#128145; Romantic"},
        {"name": "Bali", "country": "Indonesia", "price": "₹20K", "hotel": "₹6,000/night", "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop", "tag": "&#127958; Beach"},
        {"name": "Maldives", "country": "Maldives", "price": "₹45K", "hotel": "₹25,000/night", "image": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400&h=250&fit=crop", "tag": "&#127796; Paradise"},
        {"name": "Goa", "country": "India", "price": "₹8K", "hotel": "₹4,000/night", "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400&h=250&fit=crop", "tag": "&#127881; Party"},
        {"name": "Jaipur", "country": "India", "price": "₹6K", "hotel": "₹3,000/night", "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=250&fit=crop", "tag": "&#127984; Heritage"},
    ]
    
    cols = st.columns(3)
    for idx, dest in enumerate(trending_destinations):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="destination-card">'
                f'<div style="position: relative;">'
                f'<img src="{dest["image"]}" style="width: 100%; height: 200px; object-fit: cover;" alt="{dest["name"]}">'
                f'<div style="position: absolute; top: 10px; right: 10px; background: rgba(255,255,255,0.9); padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">'
                f'{dest["tag"]}'
                f'</div>'
                f'</div>'
                f'<div style="padding: 15px;">'
                f'<h3 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 20px;">{dest["name"]}</h3>'
                f'<p style="margin: 0 0 10px 0; color: #666; font-size: 13px;">&#128205; {dest["country"]}</p>'
                f'<p style="margin: 5px 0; color: #333;"><strong style="color: #ff6b6b;">Flights from:</strong> {dest["price"]}</p>'
                f'<p style="margin: 5px 0; color: #333;"><strong style="color: #4ecdc4;">Hotels from:</strong> {dest["hotel"]}</p>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ============================================================================
# TAB 8: TRAVEL TIPS
# ============================================================================
with tab8:
    st.header("&#128161; Essential Travel Tips & Guides")
    
    # Create sub-tabs for different tip categories
    tip_tabs = st.tabs(["&#127890; Packing", "&#128176; Money", "&#127973; Health", "&#128241; Technology", "&#127757; Culture", "&#128203; Checklist"])
    
    with tip_tabs[0]:
        st.markdown("### &#127890; Smart Packing Tips")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**&#9989; Essential Items:**\n"
                "- &#128241; Phone charger & power bank\n"
                "- &#129738; Passport & visa documents\n"
                "- &#128179; Credit/debit cards\n"
                "- &#128138; Basic medications\n"
                "- &#129524; Toiletries (travel-sized)\n"
                "- &#128085; Versatile clothing\n"
                "- &#128268; Universal adapter\n"
                "- &#127911; Headphones\n"
            )
        
        with col2:
            st.markdown(
                "**&#128161; Pro Tips:**\n"
                "- Roll clothes instead of folding\n"
                "- Use packing cubes for organization\n"
                "- Wear heaviest items on flight\n"
                "- Pack a change of clothes in carry-on\n"
                "- Keep valuables in hand luggage\n"
                "- Check airline baggage limits\n"
                "- Leave space for souvenirs\n"
                "- Pack a reusable water bottle\n"
            )
        
        st.info("&#128230; **Packing Hack:** Use compression bags to save 50% space!")
    
    with tip_tabs[1]:
        st.markdown("### &#128176; Money Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**&#128179; Payment Methods:**\n"
                "- Carry multiple credit cards\n"
                "- Inform bank about travel dates\n"
                "- Keep some local currency\n"
                "- Use forex cards for better rates\n"
                "- Download payment apps\n"
                "- Keep emergency cash hidden\n"
            )
        
        with col2:
            st.markdown(
                "**&#128161; Money-Saving Tips:**\n"
                "- Book flights in advance\n"
                "- Travel during off-season\n"
                "- Use public transportation\n"
                "- Eat at local restaurants\n"
                "- Look for free attractions\n"
                "- Use travel reward cards\n"
                "- Compare prices online\n"
                "- Avoid airport exchanges\n"
            )
        
        st.success("&#128176; **Budget Tip:** Set daily spending limits and track expenses!")
    
    with tip_tabs[2]:
        st.markdown("### &#127973; Health & Safety")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**&#127973; Before You Go:**\n"
                "- Get travel insurance\n"
                "- Check vaccination requirements\n"
                "- Carry prescription medications\n"
                "- Pack a first-aid kit\n"
                "- Know your blood type\n"
                "- Copy important documents\n"
            )
        
        with col2:
            st.markdown(
                "**&#128680; Safety Precautions:**\n"
                "- Research safe neighborhoods\n"
                "- Keep emergency numbers handy\n"
                "- Register with your embassy\n"
                "- Avoid displaying valuables\n"
                "- Use hotel safes\n"
                "- Stay aware of surroundings\n"
                "- Share itinerary with family\n"
            )
        
        st.warning("&#9888; **Important:** Always have travel insurance with medical coverage!")
    
    with tip_tabs[3]:
        st.markdown("### &#128241; Technology & Connectivity")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**&#128241; Essential Apps:**\n"
                "- Google Maps (offline mode)\n"
                "- Google Translate\n"
                "- Currency converter\n"
                "- Local transportation apps\n"
                "- Weather apps\n"
                "- Flight tracking apps\n"
                "- Hotel booking apps\n"
            )
        
        with col2:
            st.markdown(
                "**&#128161; Tech Tips:**\n"
                "- Download offline maps\n"
                "- Get local SIM or eSIM\n"
                "- Use VPN for security\n"
                "- Backup photos to cloud\n"
                "- Carry portable charger\n"
                "- Save important numbers offline\n"
                "- Enable roaming (if needed)\n"
            )
        
        st.info("&#128246; **Pro Tip:** Download entertainment for flights before departure!")
    
    with tip_tabs[4]:
        st.markdown("### &#127757; Cultural Etiquette")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**&#128591; Respect Local Customs:**\n"
                "- Research cultural norms\n"
                "- Learn basic local phrases\n"
                "- Dress appropriately\n"
                "- Follow photography rules\n"
                "- Respect religious sites\n"
                "- Understand tipping customs\n"
            )
        
        with col2:
            st.markdown(
                "**&#128161; Cultural Tips:**\n"
                "- Greet in local language\n"
                "- Remove shoes when required\n"
                "- Ask before taking photos\n"
                "- Be mindful of gestures\n"
                "- Respect personal space\n"
                "- Follow dining etiquette\n"
                "- Be patient and flexible\n"
            )
        
        st.success("&#127759; **Remember:** You're a guest in their country - be respectful!")
    
    with tip_tabs[5]:
        st.markdown("### &#128203; Pre-Travel Checklist")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**&#9989; 2 Weeks Before:**\n"
                "- [ ] Book flights & hotels\n"
                "- [ ] Apply for visa (if needed)\n"
                "- [ ] Get travel insurance\n"
                "- [ ] Check passport validity\n"
                "- [ ] Book airport transfers\n"
                "- [ ] Research destination\n"
                "- [ ] Make restaurant reservations\n"
            )
            
            st.markdown(
                "**&#9989; 1 Week Before:**\n"
                "- [ ] Confirm all bookings\n"
                "- [ ] Notify bank & credit cards\n"
                "- [ ] Get local currency\n"
                "- [ ] Download offline maps\n"
                "- [ ] Pack medications\n"
                "- [ ] Charge all devices\n"
            )
        
        with col2:
            st.markdown(
                "**&#9989; 1 Day Before:**\n"
                "- [ ] Web check-in for flight\n"
                "- [ ] Print boarding passes\n"
                "- [ ] Pack carry-on bag\n"
                "- [ ] Check weather forecast\n"
                "- [ ] Set travel alerts\n"
                "- [ ] Inform family/friends\n"
                "- [ ] Arrange pet care\n"
            )
            
            st.markdown(
                "**&#9989; Day of Travel:**\n"
                "- [ ] Check flight status\n"
                "- [ ] Arrive 3 hours early (international)\n"
                "- [ ] Keep documents handy\n"
                "- [ ] Turn on roaming/get SIM\n"
                "- [ ] Enjoy your trip! &#127881;\n"
            )
        
        st.balloons()
        st.success("&#127882; **You're all set!** Have an amazing journey!")

# Footer
st.markdown("---")
st.markdown(
    f'<div style="'
    f'    text-align: center;'
    f'    padding: 20px;'
    f'    margin-top: 30px;'
    f'    background-color: #f0f2f6;'
    f'    border-radius: 10px;'
    f'    border: 1px solid #d1d5db;'
    f'    color: #000000;'
    f'    font-weight: bold;'
    f'    font-size: 16px;'
    f'    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'
    f'">'
    f'    Made with &#10084;&#65039; by Ratnesh Singh (Data Scientist) | AGENTIC AI Trip Planner(CrewAI) &#9992;&#65039;'
    f'</div>',
    unsafe_allow_html=True
)