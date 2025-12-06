from crewai import Task

# ============================================================================
# TASK 1: Travel Logistics & Information Research
# ============================================================================
def location_task(agent, from_city, destination_city, date_from, date_to):
    return Task(
        description=f"""
        **CRITICAL INSTRUCTION**: After doing 3-5 web searches, you MUST compile all information and write a COMPLETE FINAL ANSWER. Do NOT keep searching endlessly.
        
        Research and compile comprehensive travel logistics information for a trip.
        
        **Trip Details:**
        - From: {from_city}
        - To: {destination_city}
        - Dates: {date_from} to {date_to}
        
        **YOUR TASK:**
        1. Do 3-5 web searches to gather information
        2. Then IMMEDIATELY write the complete final report with ALL sections below
        3. Use the information you found to fill in specific details
        
        **Required Information (Must Include ALL in your FINAL ANSWER):**
        
        1. **Transportation Options (with specific examples like this):**
           
           **Example Format:**
           ## Transportation
           **Flights:**
           - IndiGo: {from_city} → {destination_city}, ₹8,999, 6h (1 stop)
           - Air India: {from_city} → {destination_city}, ₹10,810, 6.5h (direct)
           - SpiceJet: {from_city} → {destination_city}, ₹7,500, 7h (2 stops)
           - **Recommended**: IndiGo (best value, reasonable time)
           
           **Trains** (if applicable):
           - Rajdhani Express: ₹3,500 (3AC), 24h
           - Duronto Express: ₹4,200 (2AC), 22h
           - **Recommended**: Rajdhani (comfortable, reliable)
           
           **Buses** (if applicable):
           - Volvo Sleeper: ₹2,000, 18h
           - Not recommended for long distances
        
        2. **Accommodation (with specific examples like this):**
           
           **Example Format:**
           ## Accommodation
           
           **Budget (₹1000-2000/night):**
           1. Hotel 81 Dickson - ₹1,500/night, Little India area
           2. The Pod Boutique Capsule Hotel - ₹1,800/night, Beach Road
           3. Hotel NuVe - ₹1,200/night, Bugis (near MRT)
           
           **Mid-Range (₹2000-4000/night):**
           1. Holiday Inn Express Clarke Quay - ₹3,500/night, Clarke Quay
           2. Mercure Singapore Bugis - ₹2,800/night, Bugis
           3. Hotel Mono - ₹2,500/night, Chinatown
           
           **Luxury (₹4000+/night):**
           1. Marina Bay Sands - ₹15,000/night, Marina Bay (iconic infinity pool)
           2. Raffles Hotel - ₹20,000/night, City Center (historic luxury)
        
        3. **Cost of Living (with specific examples like this):**
           
           **Example Format:**
           ## Daily Costs
           
           **Meals:**
           - Breakfast (hawker center): ₹150-300
           - Lunch (local restaurant): ₹400-800
           - Dinner (mid-range): ₹800-1,500
           - Street food snacks: ₹100-200
           
           **Local Transportation:**
           - MRT single ride: ₹50-150
           - MRT day pass: ₹400
           - Taxi (5km): ₹300-500
           - Grab/Uber (average): ₹200-400
           
           **Entry Fees:**
           - Gardens by the Bay: ₹1,800
           - Universal Studios: ₹5,500
           - Singapore Zoo: ₹2,500
           - Marina Bay Sands SkyPark: ₹1,500
           
           **Daily Budget Estimates:**
           - Budget traveler: ₹3,000-4,000/day
           - Mid-range traveler: ₹6,000-8,000/day
           - Luxury traveler: ₹12,000+/day
        
        4. **Weather Forecast (with specific examples like this):**
           
           **Example Format:**
           ## Weather in {destination_city} ({date_from} to {date_to})
           
           **Temperature:**
           - Daytime: 28-32°C (hot and humid)
           - Evening: 24-26°C (warm)
           - Feels like: 32-35°C (high humidity)
           
           **Rainfall:**
           - Probability: 40% (occasional showers)
           - Type: Short tropical downpours
           - Best time: Morning (less rain)
           
           **What to Pack:**
           - Light, breathable clothing
           - Umbrella (sun and rain)
           - Sunscreen SPF 50+
           - Light jacket for AC indoors
           - Comfortable walking shoes
           - Hat and sunglasses
        
        5. **Visa/Documentation (with specific examples like this):**
           
           **Example Format:**
           ## Travel Documents
           
           **For Indian Citizens:**
           - Passport required (valid 6+ months)
           - Visa: e-Visa available online (₹4,500, 30 days)
           - Processing time: 3-5 business days
           - No COVID-19 vaccination required (as of 2025)
           
           **Required Documents:**
           - Valid passport
           - Return flight tickets
           - Hotel booking confirmation
           - Travel insurance (recommended)
           - Sufficient funds proof
           
           **Health Requirements:**
           - No mandatory vaccinations
           - Travel insurance recommended
           - Carry basic medications
        
        **IMPORTANT**: After your research, write a COMPLETE markdown report with ALL sections above using this exact format with specific names, prices, and details. Do NOT just list search queries!
        """,
        expected_output="""A comprehensive markdown report with:
        - Transportation comparison table with prices
        - Accommodation options with names and prices
        - Cost breakdown for meals and activities
        - Weather forecast and packing suggestions
        - All information must be specific with actual numbers and names""",
        agent=agent,
        output_file='city_report.md',
    )

# ============================================================================
# TASK 2: Local Attractions & Activities Guide
# ============================================================================
def guide_task(agent, destination_city, interests, date_from, date_to):
    return Task(
        description=f"""
        **CRITICAL INSTRUCTION**: After doing 3-5 web searches, you MUST compile all information and write a COMPLETE FINAL ANSWER with ALL attractions, restaurants, and activities listed. Do NOT keep searching endlessly.
        
        Create a detailed local guide with attractions, restaurants, and activities.
        
        **Destination:** {destination_city}
        **Travel Dates:** {date_from} to {date_to}
        **Traveler Interests:** {interests}
        
        **YOUR TASK:**
        1. Do 3-5 web searches to find attractions, restaurants, and activities
        2. Then IMMEDIATELY write the complete final guide with ALL sections below
        3. List specific names, addresses, and prices
        
        **Required Content (Must Include ALL in your FINAL ANSWER):**
        
        1. **Top Attractions (List 10-15 with specific examples like this):**
           
           **Example Format:**
           ## Top Attractions
           
           **1. Gardens by the Bay**
           - Futuristic garden with Supertree Grove and Cloud Forest dome. Perfect for sightseeing with stunning architecture and photo opportunities. The evening light show is spectacular.
           - Entry: ₹1,800/person (conservatories)
           - Best time: Evening (6-8 PM for light show)
           - Matches {interests}: Amazing sightseeing, Instagram-worthy spots
           
           **2. Marina Bay Sands SkyPark**
           - Observation deck 200m high with 360° city views. Iconic infinity pool (for hotel guests). Best sunset views in the city.
           - Entry: ₹1,500/person
           - Best time: Sunset (6-7 PM)
           - Matches {interests}: Breathtaking views, perfect for sightseeing
           
           **3. Universal Studios Singapore**
           - Theme park with thrilling rides and shows. Adventure-packed day with roller coasters and attractions.
           - Entry: ₹5,500/person
           - Best time: Weekday mornings (less crowded)
           - Matches {interests}: Adventure, excitement, full-day entertainment
           
           [Continue with 7-12 more attractions...]
        
        2. **Food Recommendations (List 8-10 places with specific examples like this):**
           
           **Example Format:**
           ## Food Recommendations
           
           **1. Maxwell Food Centre**
           - Cuisine: Hawker center (local food court)
           - Must-try dishes:
             * Hainanese Chicken Rice (₹200)
             * Char Kway Teow (₹250)
             * Satay (₹300 for 10 sticks)
             * Fresh coconut water (₹100)
           - Cost for 2: ₹600-800
           - Location: Chinatown, 1 Kadayanallur St
           - Why: Authentic local food, budget-friendly, famous stalls
           
           **2. Lau Pa Sat (Telok Ayer Market)**
           - Cuisine: Hawker center with variety
           - Must-try dishes:
             * Satay Street (evening)
             * Nasi Lemak (₹300)
             * BBQ Seafood (₹800)
             * Carrot Cake (₹200)
           - Cost for 2: ₹1,000-1,500
           - Location: 18 Raffles Quay, CBD
           - Why: Historic building, great atmosphere, diverse options
           
           **3. Jumbo Seafood**
           - Cuisine: Singaporean seafood
           - Must-try dishes:
             * Chili Crab (₹2,500 - signature dish!)
             * Black Pepper Crab (₹2,200)
             * Cereal Prawns (₹1,800)
             * Fried Rice (₹400)
           - Cost for 2: ₹4,000-5,000
           - Location: Riverside Point, Clarke Quay
           - Why: Famous for chili crab, waterfront dining
           
           [Continue with 5-7 more restaurants...]
        
        3. **Activities Based on Interests (with specific examples like this):**
           
           **Example Format:**
           ## Activities for {interests}
           
           **Sightseeing Activities:**
           - Singapore River Cruise (₹1,200, 40 min, see city from water)
           - Merlion Park photo stop (Free, iconic Singapore symbol)
           - Chinatown Heritage Centre (₹800, learn history)
           - Little India walking tour (Free, colorful streets)
           - ArtScience Museum (₹1,000, unique architecture)
           
           **Food Activities:**
           - Chinatown Food Street tour (₹2,500, guided 3-hour tour)
           - Cooking class at Food Playground (₹3,500, learn local dishes)
           - Hawker center hopping (Self-guided, ₹1,000 for tastings)
           - Tiong Bahru Market breakfast (₹500, local favorite)
           
           **Adventure Activities:**
           - Sentosa Mega Adventure Park (₹2,500, zipline and rope course)
           - iFly Singapore indoor skydiving (₹4,500, thrilling experience)
           - Kayaking at Pulau Ubin (₹1,500, nature adventure)
           - Cable car to Sentosa (₹1,800, scenic ride)
           
           **Party/Nightlife:**
           - Clarke Quay bar hopping (₹2,000-3,000 per person)
           - Zouk nightclub (₹1,500 entry, top DJ performances)
           - CÉ LA VI rooftop bar (₹2,000 minimum, stunning views)
           - Boat Quay riverside bars (₹1,000-1,500, relaxed vibe)
        
        4. **Local Events (if any during {date_from} to {date_to}):**
           
           **Example Format:**
           ## Events During Your Visit
           
           **New Year's Eve Countdown (Dec 31)**
           - Location: Marina Bay
           - Event: Fireworks and light show
           - Time: 11:30 PM - 12:30 AM
           - Cost: Free (public viewing)
           - Tips: Arrive by 9 PM for good spot
           
           **Christmas Light-Up (if December)**
           - Location: Orchard Road
           - Event: Street decorations and displays
           - Time: Daily, 6 PM - 12 AM
           - Cost: Free
           
           **Weekend Markets:**
           - Artbox Singapore (if running)
           - Location: Bayfront Event Space
           - Time: Fri-Sun, 4 PM - 11 PM
           - Cost: Free entry, food/shopping extra
        
        5. **Hidden Gems (with specific examples like this):**
           
           **Example Format:**
           ## Hidden Gems
           
           **1. Haji Lane**
           - Narrow street in Kampong Glam with colorful murals, indie boutiques, and hipster cafes
           - Location: Arab Quarter
           - Cost: Free to explore, ₹500-1,000 for cafe/shopping
           - Why locals love it: Unique shopping, Instagram-worthy, less touristy
           
           **2. Tiong Bahru**
           - Retro neighborhood with art deco buildings, indie bookstores, and artisan cafes
           - Location: Tiong Bahru Estate
           - Cost: Free to walk, ₹600 for brunch
           - Why locals love it: Authentic local vibe, great food, vintage charm
           
           **3. Pulau Ubin**
           - Rustic island with cycling trails, mangroves, and traditional kampong houses
           - Location: 10-min bumboat from Changi Point (₹150 each way)
           - Cost: ₹500 total (boat + bike rental)
           - Why locals love it: Escape the city, nature, peaceful
           
           **4. Kampong Glam**
           - Historic Malay-Arab quarter with Sultan Mosque, textile shops, and Middle Eastern cafes
           - Location: Bugis area
           - Cost: Free to explore
           - Why locals love it: Cultural diversity, unique shopping, great food
           
           **5. MacRitchie Reservoir TreeTop Walk**
           - Suspension bridge through forest canopy with nature trails
           - Location: MacRitchie Reservoir Park
           - Cost: Free
           - Why locals love it: Nature escape, exercise, peaceful
        
        **IMPORTANT**: After your research, write a COMPLETE guide with ALL 10-15 attractions (with descriptions, fees, times), 8-10 restaurants (with dishes and prices), specific activities for each interest, events during travel dates, and 3-5 hidden gems. Do NOT just list search queries!
        """,
        expected_output="""A detailed markdown guide with:
        - 10-15 specific attractions with names and details
        - 8-10 restaurant recommendations with names and dishes
        - Activities tailored to user interests
        - Local events during travel dates
        - Hidden gems with specific locations
        - All recommendations must be specific and actionable""",
        agent=agent,
        output_file='guide_report.md',
    )

# ============================================================================
# TASK 3: Complete Itinerary Planning
# ============================================================================
def planner_task(context, agent, destination_city, interests, date_from, date_to):
    return Task(
        description=f"""
        **CRITICAL INSTRUCTION**: After doing 2-3 web searches, you MUST write a COMPLETE day-by-day itinerary with ALL days, paragraphs, budget breakdown, and tips. Do NOT keep searching endlessly.
        
        Create a comprehensive, day-by-day travel itinerary using information from previous tasks.
        
        **Trip Details:**
        - Destination: {destination_city}
        - Interests: {interests}
        - Dates: {date_from} to {date_to}
        
        **YOUR TASK:**
        1. Do 2-3 web searches if needed
        2. Then IMMEDIATELY write the complete final itinerary with ALL sections below
        3. Include specific names, timings, and prices for everything
        
        **Required Structure (Must Include ALL in your FINAL ANSWER):**
        
        1. **City Introduction (4 DETAILED paragraphs - minimum 5-7 sentences each):**
           
           **Paragraph 1 - City Overview (5-7 sentences):**
           - What makes {destination_city} unique and special
           - Key highlights and main attractions
           - Why travelers love visiting
           - Best time to visit
           - Overall vibe and atmosphere
           
           **Paragraph 2 - History & Culture (5-7 sentences):**
           - Historical background and founding
           - Cultural heritage and traditions
           - Important historical landmarks
           - Local customs and way of life
           - How history shapes the modern city
           
           **Paragraph 3 - Food Scene (5-7 sentences):**
           - Signature dishes and must-try foods
           - Famous food markets and hawker centers
           - Popular restaurants and cafes
           - Street food culture
           - Unique culinary experiences
           - Price ranges for different dining options
           
           **Paragraph 4 - Best Experiences for {interests} (5-7 sentences):**
           - Specific activities matching {interests}
           - Top recommendations for this interest
           - Hidden gems for these interests
           - Best areas/neighborhoods to explore
           - Unique experiences not to miss
        
        2. **Day-by-Day Itinerary (COMPLETE details for EVERY day):**
           For EACH day from {date_from} to {date_to}, provide:
           
           **Day X: [Specific Theme/Focus]**
           
           - **Morning (9:00 AM - 12:00 PM):**
             * **Activity 1**: [Specific attraction name with full address]
             * **What to do**: Detailed description of the activity
             * **Duration**: X hours X minutes
             * **Travel time from hotel**: X minutes by [transport mode]
             * **Entry fee**: ₹X per person
             * **Why visit**: What makes it special
             * **Tips**: Best time, what to bring, insider tips
           
           - **Afternoon (12:00 PM - 5:00 PM):**
             * **Lunch (12:00 PM)**: [Specific restaurant name + address]
               - Cuisine type
               - Must-try dishes (list 3-4 dishes)
               - Cost for 2 people: ₹X
               - Why recommended
             
             * **Activity 2**: [Specific place name with address]
             * **What to do**: Detailed description
             * **Duration**: X hours
             * **Travel time**: X minutes by [transport]
             * **Entry fee**: ₹X per person
             * **Tips**: What to see, best photo spots
           
           - **Evening (5:00 PM - 9:00 PM):**
             * **Activity 3**: [Specific attraction/viewpoint name]
             * **What to do**: Evening activity description
             * **Duration**: X hours
             * **Cost**: ₹X per person
             
             * **Dinner (7:00 PM)**: [Specific restaurant name + address]
               - Cuisine type
               - Recommended dishes (list 3-4)
               - Cost for 2 people: ₹X
               - Ambiance and why it's perfect for evening
           
           - **Night (9:00 PM onwards - for party/nightlife):**
             * **Venue 1**: [Specific club/bar name + address]
               - Type (club/bar/lounge/rooftop)
               - Music genre/vibe
               - Entry fee: ₹X
               - Drink prices: ₹X-₹X
               - Dress code
               - Best time to arrive
             
             * **Venue 2** (alternative): [Name + address]
               - Similar details as above
           
           **Daily Total Cost**: ₹X per person
        
        3. **Budget Breakdown (DETAILED with calculations):**
           
           **Transportation:**
           - Round-trip flights: ₹X × 2 people = ₹X
           - Airport transfers: ₹X × 2 ways = ₹X
           - Local transport (MRT/taxi/bus): ₹X per day × X days = ₹X
           - **Subtotal Transportation**: ₹X
           
           **Accommodation:**
           - Hotel: [Recommended hotel name]
           - Rate: ₹X per night
           - Number of nights: X nights
           - **Subtotal Accommodation**: ₹X × X nights = ₹X
           
           **Food & Dining:**
           - Breakfast: ₹X per day × X days = ₹X
           - Lunch: ₹X per day × X days = ₹X
           - Dinner: ₹X per day × X days = ₹X
           - Snacks/drinks: ₹X per day × X days = ₹X
           - **Subtotal Food**: ₹X
           
           **Activities & Entry Fees:**
           - [List each major attraction]
             * [Attraction 1]: ₹X × 2 = ₹X
             * [Attraction 2]: ₹X × 2 = ₹X
             * [Attraction 3]: ₹X × 2 = ₹X
           - Tours/experiences: ₹X
           - **Subtotal Activities**: ₹X
           
           **Nightlife & Entertainment:**
           - Club entries: ₹X
           - Drinks/beverages: ₹X
           - **Subtotal Entertainment**: ₹X
           
           **Shopping & Miscellaneous:**
           - Souvenirs: ₹X
           - Emergency fund: ₹X
           - **Subtotal Misc**: ₹X
           
           **TOTAL ESTIMATED COST FOR 2 PEOPLE**: ₹X
           **Per Person Cost**: ₹X
           
           **Budget Options:**
           - Budget traveler: ₹X per person
           - Mid-range traveler: ₹X per person
           - Luxury traveler: ₹X per person
        
        4. **Practical Tips (COMPREHENSIVE guide):**
           
           **Getting Around:**
           - Best transport option: [MRT/Metro/Taxi/etc]
           - How to buy tickets/passes
           - Cost of day pass: ₹X
           - Apps to download: [List specific apps]
           - Average taxi fare: ₹X per km
           - Walking-friendly areas: [List areas]
           
           **Safety Tips:**
           - Overall safety level: [Very safe/Safe/Moderate]
           - Areas to avoid at night: [Specific areas or "None"]
           - Common scams to watch for: [List 2-3]
           - Emergency numbers:
             * Police: XXX
             * Ambulance: XXX
             * Tourist helpline: XXX
           - Hospital locations: [List 2 major hospitals with addresses]
           
           **Money-Saving Tips:**
           - Best areas for budget food: [Specific locations]
           - Free attractions: [List 3-5 free things]
           - Discount cards available: [Tourist pass names]
           - Happy hour timings: [X PM to X PM]
           - Best day for shopping deals: [Day of week]
           - ATM fees and best banks: [Specific info]
           
           **Local Customs & Etiquette:**
           - Dress code for religious sites: [Specific requirements]
           - Tipping culture: [Expected % or "Not required"]
           - Greeting customs: [How to greet locals]
           - Dining etiquette: [Important rules]
           - Photography restrictions: [Where not to photo]
           - Language: [Common phrases in local language]
           
           **Best Times to Visit Attractions:**
           - [Attraction 1]: Best at [time] because [reason]
           - [Attraction 2]: Best at [time] because [reason]
           - Avoid weekends at: [List crowded places]
           
           **Useful Apps & Websites:**
           - Navigation: [App names]
           - Food delivery: [App names]
           - Ride-hailing: [App names]
           - Translation: [App names]
        
        5. **Packing Checklist (DETAILED by category):**
           
           **Weather-Specific Items:**
           - Temperature range: X°C to X°C
           - Expected weather: [Sunny/Rainy/etc]
           - Clothing:
             * X lightweight shirts/tops
             * X pairs of shorts/pants
             * X dresses/skirts (if applicable)
             * 1 light jacket (for AC/evening)
             * Swimwear (if beach/pool activities)
             * Comfortable walking shoes
             * Sandals/flip-flops
             * Socks and underwear
           
           **Sun Protection:**
           - Sunscreen (SPF 50+)
           - Sunglasses
           - Hat/cap
           - Umbrella (sun/rain)
           
           **Adventure/Activity Gear:**
           - [Based on {interests}]
           - Sports shoes (if adventure activities)
           - Waterproof bag
           - GoPro/action camera
           - Dry bag for water activities
           
           **Nightlife/Party Essentials:**
           - Smart casual outfits
           - Party shoes/heels
           - Small crossbody bag
           - Power bank for phone
           
           **Health & Hygiene:**
           - Medications (personal prescriptions)
           - First aid kit basics
           - Hand sanitizer
           - Wet wipes
           - Mosquito repellent
           - Motion sickness pills
           
           **Electronics:**
           - Phone charger
           - Power bank (10000mAh+)
           - Universal adapter ([Plug type] for {destination_city})
           - Camera + memory cards
           - Headphones
           
           **Documents & Money:**
           - Passport (valid 6+ months)
           - Visa (if required)
           - Travel insurance papers
           - Hotel confirmations
           - Flight tickets (printed + digital)
           - Credit/debit cards (2-3 cards)
           - Cash in local currency: ₹X recommended
           - Photocopy of important documents
           
           **Miscellaneous:**
           - Reusable water bottle
           - Snacks for travel
           - Travel pillow
           - Eye mask and earplugs
           - Ziplock bags
           - Small backpack for day trips
        
        **IMPORTANT**: Write the COMPLETE itinerary with ALL 4 detailed paragraphs (5-7 sentences each), ALL days with full morning/afternoon/evening/night details, COMPLETE budget breakdown with calculations, ALL practical tips in every category, and COMPLETE packing checklist. Do NOT just list search queries!
        
        **IMPORTANT**: Write the COMPLETE itinerary with ALL 4 paragraphs, ALL days, budget breakdown, and ALL tips. Do NOT just list search queries!
        """,
        expected_output="""A complete markdown travel itinerary with:
        - 4-paragraph city introduction
        - Detailed day-by-day schedule with specific timings (9 AM, 12 PM, etc.)
        - Specific restaurant and attraction names for each time slot
        - Complete budget breakdown with actual numbers
        - Practical tips and packing list
        - Everything must be specific, detailed, and ready to follow""",
        context=context,
        agent=agent,
        output_file='travel_plan.md',
    )
