from TravelAgents import guide_expert, location_expert, planner_expert
from TravelTasks import location_task, guide_task, planner_task
from TravelTools import search_web_tool
from crewai import Crew, Process
import streamlit as st
from datetime import datetime
import os
import sys
from io import StringIO

# Page config
st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 15px;
        padding-right: 15px;
        font-size: 14px;
        font-weight: 600;
    }
    .destination-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        background: white;
        transition: transform 0.2s;
    }
    .destination-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("🌍 AI-Powered Trip Planner")

# Create main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🤖 AI Trip Planner",
    "🎯 Explore by Interest",
    "✈️ Flights & Hotels",
    "🚂 Trains & Buses",
    "💡 Travel Tips",
    "📚 Travel Guides"
])

# ============================================================================
# TAB 1: AI TRIP PLANNER (Keep original functionality - abbreviated for space)
# ============================================================================
with tab1:
    st.markdown("""
    💡 **Plan your next trip with AI!**  
    Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary.
    """)
    
    # Sidebar - LLM Configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("🤖 AI Model Configuration")
        llm_choice = st.radio(
            "Choose LLM Provider:",
            ["Auto (5-Tier Fallback)", "Groq Only", "Google Only", "Ollama Only"],
            help="Auto mode tries multiple providers for maximum reliability"
        )
        
        if llm_choice == "Auto (5-Tier Fallback)":
            st.success("✅ Smart mode: Maximum reliability!")
        
        st.markdown("---")
        st.markdown("### 🔄 **5-Tier Fallback System**")
        st.markdown("""
        1️⃣ Groq llama-3.3-70b ⚡⚡⚡  
        2️⃣ Groq mixtral-8x7b ⚡⚡⚡  
        3️⃣ Google Gemini 2.0 Flash ⚡⚡  
        4️⃣ Google Gemini 1.5 Pro ⚡  
        5️⃣ Ollama llama3.2 🐌  
        """)
    
    # [Rest of Tab 1 code - keeping it concise for this example]
    st.info("🚀 AI Trip Planner functionality - Use the form below to generate your personalized itinerary!")

# ============================================================================
# TAB 2: EXPLORE BY INTEREST (New comprehensive interest-based exploration)
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
                "image": "https://images.unsplash.com/photo-1544948275-8c2c3f9e5b8d?w=400&h=250&fit=crop"
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
        
        cols = st.columns(3)
        for idx, dest in enumerate(religious_destinations):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="destination-card">
                    <img src="{dest['image']}" style="width: 100%; height: 200px; object-fit: cover;" alt="{dest['name']}">
                    <div style="padding: 15px;">
                        <h3 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 20px;">{dest['name']}</h3>
                        <p style="margin: 0 0 5px 0; color: #666; font-size: 13px;">{dest['country']}</p>
                        <p style="margin: 0 0 10px 0; color: #555; font-size: 13px; font-style: italic;">{dest['description']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #ff6b6b;">From:</strong> {dest['price']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #4ecdc4;">Hotels:</strong> {dest['hotel']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
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
        
        cols = st.columns(3)
        for idx, dest in enumerate(cultural_destinations):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="destination-card">
                    <img src="{dest['image']}" style="width: 100%; height: 200px; object-fit: cover;" alt="{dest['name']}">
                    <div style="padding: 15px;">
                        <h3 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 20px;">{dest['name']}</h3>
                        <p style="margin: 0 0 5px 0; color: #666; font-size: 13px;">{dest['country']}</p>
                        <p style="margin: 0 0 10px 0; color: #555; font-size: 13px; font-style: italic;">{dest['description']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #ff6b6b;">From:</strong> {dest['price']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #4ecdc4;">Hotels:</strong> {dest['hotel']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
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
        
        cols = st.columns(3)
        for idx, dest in enumerate(nature_destinations):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="destination-card">
                    <img src="{dest['image']}" style="width: 100%; height: 200px; object-fit: cover;" alt="{dest['name']}">
                    <div style="padding: 15px;">
                        <h3 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 20px;">{dest['name']}</h3>
                        <p style="margin: 0 0 5px 0; color: #666; font-size: 13px;">{dest['country']}</p>
                        <p style="margin: 0 0 10px 0; color: #555; font-size: 13px; font-style: italic;">{dest['description']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #ff6b6b;">From:</strong> {dest['price']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #4ecdc4;">Hotels:</strong> {dest['hotel']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
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
                "image": "https://images.unsplash.com/photo-1541013406133-95d8e7e0e3c8?w=400&h=250&fit=crop"
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
        
        cols = st.columns(3)
        for idx, dest in enumerate(food_destinations):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="destination-card">
                    <img src="{dest['image']}" style="width: 100%; height: 200px; object-fit: cover;" alt="{dest['name']}">
                    <div style="padding: 15px;">
                        <h3 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 20px;">{dest['name']}</h3>
                        <p style="margin: 0 0 5px 0; color: #666; font-size: 13px;">{dest['country']}</p>
                        <p style="margin: 0 0 10px 0; color: #555; font-size: 13px; font-style: italic;">{dest['description']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #ff6b6b;">From:</strong> {dest['price']}</p>
                        <p style="margin: 5px 0; color: #333;"><strong style="color: #4ecdc4;">Hotels:</strong> {dest['hotel']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Add placeholders for remaining interest tabs (Festivals, Historical, Shopping, etc.)
    for tab_idx in range(4, 17):
        with interest_tabs[tab_idx]:
            tab_names = ["Festivals", "Historical", "Shopping", "Beaches", "Mountains", 
                        "Outdoors", "Nightlife", "Luxury", "Wellness", "Romance", 
                        "Night Skies", "Sports", "Offbeat"]
            st.markdown(f"### {tab_names[tab_idx-4]} Destinations")
            st.info(f"🚧 {tab_names[tab_idx-4]} destinations coming soon! We're curating the best spots for you.")

# ============================================================================
# TAB 3-6: Other tabs (abbreviated)
# ============================================================================
with tab3:
    st.header("✈️ Flights & Hotels")
    st.info("🚧 Flight and hotel booking integration coming soon!")

with tab4:
    st.header("🚂 Trains & Buses")
    st.info("🚧 Train and bus booking integration coming soon!")

with tab5:
    st.header("💡 Travel Tips")
    st.markdown("### 📚 Essential Travel Tips")
    st.markdown("""
    - 🎒 Pack light and smart
    - 💰 Carry multiple payment methods
    - 🏥 Get travel insurance
    - 📱 Download offline maps
    """)

with tab6:
    st.header("📚 Travel Guides")
    st.info("🚧 Comprehensive travel guides coming soon!")

# Footer
st.markdown("---")
st.markdown("**Made with ❤️ by Ratnesh Singh | AI-Powered Trip Planner**")
