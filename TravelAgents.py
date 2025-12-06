from crewai import Agent
from TravelTools import search_web_tool
from crewai import LLM
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# ============================================================================
# SMART LLM SELECTOR - Automatic Fallback from Groq to Ollama
# ============================================================================

def get_llm(force_groq=False, force_ollama=False, force_google=False):
    """
    Multi-tier cascading fallback system for LLM initialization.
    
    Fallback Order:
    1. Groq llama-3.3-70b-versatile (Primary - fastest)
    2. Groq mixtral-8x7b-32768 (Backup Groq model)
    3. Google Gemini (Cloud alternative)
    4. Ollama llama3.2 (Local fallback)
    
    Args:
        force_groq: If True, only try Groq models (no Google/Ollama)
        force_ollama: If True, only use Ollama (skip all cloud)
        force_google: If True, only use Google (skip Groq/Ollama)
    """
    # Get API keys from environment variables OR Streamlit secrets
    import streamlit as st
    
    # Try getting keys from environment first, then secrets
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
        
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY and hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    
    # Force Ollama mode
    if force_ollama:
        print("🔧 Force Ollama mode enabled...")
        return _init_ollama()
    
    # Force Google mode
    if force_google:
        print("🔧 Force Google mode enabled...")
        if GOOGLE_API_KEY and GOOGLE_API_KEY != "your-google-api-key-here":
            return _init_google(GOOGLE_API_KEY)
        else:
            print("❌ No valid Google API key found!")
            if _is_streamlit_cloud():
                 raise Exception("Google API Key missing on Streamlit Cloud! Please add GOOGLE_API_KEY to secrets.")
            return _init_ollama()
            
    # Helper to check if we are on cloud
    def _is_streamlit_cloud():
        return os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud" or (hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets)
    
    # ============================================================================
    # TIER 1: Try Groq llama-3.3-70b-versatile (Primary)
    # ============================================================================
    if GROQ_API_KEY and GROQ_API_KEY != "your-groq-api-key-here":
        try:
            print("🚀 [TIER 1] Attempting Groq llama-3.3-70b-versatile...")
            llm = LLM(
                model="groq/llama-3.3-70b-versatile",
                api_key=GROQ_API_KEY
            )
            print("✅ Groq llama-3.3-70b-versatile initialized successfully!")
            return llm
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "limit" in error_msg or "quota" in error_msg:
                print(f"⚠️ Groq llama-3.3 rate limit hit: {str(e)}")
                print("🔄 [TIER 2] Trying backup Groq model (mixtral)...")
            else:
                print(f"⚠️ Groq llama-3.3 failed: {str(e)}")
                print("🔄 [TIER 2] Trying backup Groq model...")
    
    # ============================================================================
    # TIER 2: Try Groq mixtral-8x7b-32768 (Backup Groq)
    # ============================================================================
    if GROQ_API_KEY and GROQ_API_KEY != "your-groq-api-key-here":
        try:
            print("🚀 [TIER 2] Attempting Groq mixtral-8x7b-32768...")
            llm = LLM(
                model="groq/mixtral-8x7b-32768",
                api_key=GROQ_API_KEY
            )
            print("✅ Groq mixtral-8x7b-32768 initialized successfully!")
            return llm
        except Exception as e:
            print(f"⚠️ Groq mixtral also failed: {str(e)}")
            if not force_groq:
                print("🔄 [TIER 3] Trying Google Gemini...")
            else:
                raise  # Don't fallback if force_groq is True
    
    # ============================================================================
    # TIER 3: Try Google Gemini 2.0 Flash (Cloud Alternative)
    # ============================================================================
    if not force_groq and GOOGLE_API_KEY and GOOGLE_API_KEY != "your-google-api-key-here":
        try:
            print("🚀 [TIER 3] Attempting Google Gemini 2.0 Flash...")
            llm = LLM(
                model="gemini/gemini-2.0-flash",
                api_key=GOOGLE_API_KEY
            )
            print("✅ Google Gemini 2.0 Flash initialized successfully!")
            return llm
        except Exception as e:
            print(f"⚠️ Google Gemini 2.0 Flash failed: {str(e)}")
            print("🔄 [TIER 4] Trying Google Gemini 1.5 Pro...")
    
    # ============================================================================
    # TIER 4: Try Google Gemini 1.5 Pro (More Capable Alternative)
    # ============================================================================
    if not force_groq and GOOGLE_API_KEY and GOOGLE_API_KEY != "your-google-api-key-here":
        try:
            print("🚀 [TIER 4] Attempting Google Gemini 1.5 Pro...")
            llm = LLM(
                model="gemini/gemini-1.5-pro",
                api_key=GOOGLE_API_KEY
            )
            print("✅ Google Gemini 1.5 Pro initialized successfully!")
            return llm
        except Exception as e:
            print(f"⚠️ Google Gemini 1.5 Pro failed: {str(e)}")
            print("🔄 [TIER 5] Falling back to local Ollama...")
    
    # ============================================================================
    # TIER 5: Ollama (Local Fallback - Always Available)
    # ============================================================================
    if not force_groq and not force_google:
        if _is_streamlit_cloud():
            raise Exception("❌ NO API KEYS FOUND! Please add GROQ_API_KEY or GOOGLE_API_KEY to Streamlit Secrets to run on Cloud.")
            
        print("🚀 [TIER 5] Using local Ollama LLM...")
        return _init_ollama()
    
    # If we get here, all options failed
    raise Exception("❌ All LLM providers failed! Check your API keys and Ollama installation.")


def _init_google(api_key):
    """Initialize Google Gemini LLM with latest model"""
    return LLM(
        model="gemini/gemini-2.0-flash",          # Stable Gemini 2.0 Flash (Recommended)
        # Alternative models (uncomment to use):
        # model="gemini/gemini-2.0-flash-exp",    # Experimental Gemini 2.0 Flash (cutting edge)
        # model="gemini/gemini-1.5-pro",          # Gemini 1.5 Pro (more capable, slower)
        # model="gemini/gemini-1.5-flash",        # Gemini 1.5 Flash (previous version)
        api_key=api_key
    )


def _init_ollama():
    """Initialize local Ollama LLM"""
    try:
        llm = LLM(
            model="ollama/llama3.2",
            base_url="http://localhost:11434",
            timeout=1800  # 30 minutes for complex tasks
        )
        print("✅ Ollama LLM initialized successfully!")
        return llm
    except Exception as e:
        print(f"❌ Ollama LLM failed: {str(e)}")
        print("💡 Make sure Ollama is running: ollama serve")
        raise

# Initialize LLM with automatic fallback (default mode)
llm = get_llm()


# ============================================================================
# TRAVEL AGENTS - Enhanced for Better Performance
# ============================================================================

# Agent 1: Location & Logistics Expert
location_expert = Agent(
    role="Travel Logistics & Information Specialist",
    goal="Research and provide comprehensive travel information including transportation, accommodations, costs, weather, and visa requirements.",
    backstory="""You are an experienced travel consultant with 15 years of expertise in planning 
    domestic and international trips. You excel at finding the best transportation options, 
    accommodation deals, and providing accurate cost estimates. You always provide complete, 
    detailed reports with specific recommendations and pricing.""",
    tools=[search_web_tool],  
    verbose=True,
    max_iter=30,  # Drastically increased to ensure completion
    llm=llm,
    allow_delegation=False,
)

# Agent 2: Local Guide & Attractions Expert
guide_expert = Agent(
    role="Local Guide & Attractions Specialist",
    goal="Discover and recommend the best attractions, restaurants, activities, and events based on traveler interests.",
    backstory="""You are a passionate local guide who has lived in major cities across India. 
    You know the hidden gems, best restaurants, must-visit attractions, and exciting events. 
    You tailor recommendations to match traveler interests perfectly, whether it's sightseeing, 
    food, adventure, or nightlife. You always provide specific names, addresses, and insider tips.""",
    tools=[search_web_tool],
    verbose=True,
    max_iter=35,  # Drastically increased for comprehensive recommendations
    llm=llm,
    allow_delegation=False,
)

# Agent 3: Itinerary Planning Expert
planner_expert = Agent(
    role="Master Itinerary Planner",
    goal="Create detailed, day-by-day travel itineraries with specific timings, activities, and budget breakdowns.",
    backstory="""You are a professional travel planner who has created over 1000 successful 
    itineraries. You excel at organizing information into clear, actionable day-by-day plans 
    with specific timings, realistic travel times, and accurate budget estimates. You always 
    include a city introduction, detailed daily schedules, restaurant recommendations, and 
    practical tips. Your itineraries are comprehensive, well-structured, and easy to follow.""",
    tools=[search_web_tool],
    verbose=True,
    max_iter=40,  # Highest for final compilation
    llm=llm,
    allow_delegation=False,
)

# Agent 4: Transport & Accommodation Booking Expert
booking_expert = Agent(
    role="Travel Booking & Logistics Manager",
    goal="Find the best travel options including flights, hotels, trains, and buses with accurate prices and schedules.",
    backstory="""You are a dedicated booking specialist who knows how to find the best deals for any mode of transport.
    Whether it's finding the cheapest flight, the most comfortable train, a luxury bus, or a perfectly located hotel,
    you analyze all options to provide the best recommendations. You always provide specific airline/train/bus names,
    timings, and current prices in Indian Rupees.""",
    tools=[search_web_tool],
    verbose=True,
    max_iter=30,
    llm=llm,
    allow_delegation=False,
)
