from crewai import Task

# ============================================================================
# SIMPLIFIED TASKS - Designed for ACTUAL COMPLETION
# ============================================================================
# These tasks are simplified to ensure agents can ACTUALLY complete them
# instead of getting stuck in endless search loops.
# ============================================================================

# ============================================================================
# TASK 1: Travel Logistics & Information Research (SIMPLIFIED)
# ============================================================================
def location_task(agent, from_city, destination_city, date_from, date_to, num_adults=2, num_children=0):
    total_persons = num_adults + num_children
    
    return Task(
        description=f"""
        **CRITICAL: After 3 web searches, STOP searching and write your complete answer!**
        
        Research travel logistics for a trip from {from_city} to {destination_city} ({date_from} to {date_to}).
        Travelers: {num_adults} adults + {num_children} children = {total_persons} total persons.
        
        **YOUR TASK (Complete in 3 steps):**
        1. Search for flights (1 search)
        2. Search for hotels (1 search)
        3. Search for costs/weather (1 search)
        4. **STOP SEARCHING** and write your complete report below
        
        **Write a complete report with these 5 sections:**
        
        ## 1. Transportation
        List 3 flight options with:
        - Airline name
        - Price per person in ₹
        - Duration
        - Recommend the best option
        
        ## 2. Accommodation  
        List 6 hotels total:
        - 2 budget hotels (₹1000-2000/night) with names and prices
        - 2 mid-range hotels (₹2000-4000/night) with names and prices
        - 2 luxury hotels (₹4000+/night) with names and prices
        
        ## 3. Daily Costs
        - Breakfast cost: ₹X
        - Lunch cost: ₹X
        - Dinner cost: ₹X
        - Local transport per day: ₹X
        - Daily budget estimate: ₹X per person
        
        ## 4. Weather
        - Temperature range: X-X°C
        - Rain probability: X%
        - What to pack: (list 3-4 items)
        
        ## 5. Visa/Documents
        - Visa required: Yes/No
        - Visa cost: ₹X (if applicable)
        - Required documents: (list 2-3)
        
        **IMPORTANT:** Write ALL 5 sections with actual numbers and names. Do NOT just search!
        """,
        expected_output=f"""A complete markdown report with:
        - 3 flight options with prices for {total_persons} person(s)
        - 6 hotel options (2 budget, 2 mid-range, 2 luxury) with names and prices
        - Daily cost breakdown
        - Weather info and packing list
        - Visa requirements
        All prices must be in ₹ (Indian Rupees)""",
        agent=agent,
        output_file='city_report.md',
    )

# ============================================================================
# TASK 2: Local Attractions & Activities Guide (SIMPLIFIED)
# ============================================================================
def guide_task(agent, destination_city, interests, date_from, date_to):
    return Task(
        description=f"""
        **CRITICAL: After 3 web searches, STOP searching and write your complete answer!**
        
        Create a local guide for {destination_city} matching interests: {interests}.
        Travel dates: {date_from} to {date_to}.
        
        **YOUR TASK (Complete in 3 steps):**
        1. Search for top attractions (1 search)
        2. Search for restaurants (1 search)
        3. Search for activities/events (1 search)
        4. **STOP SEARCHING** and write your complete guide below
        
        **Write a complete guide with these 5 sections:**
        
        ## 1. Top 5 Attractions
        For each attraction, include:
        - Name
        - 2-sentence description
        - Entry fee in ₹
        - Best time to visit
        
        ## 2. Top 5 Restaurants
        For each restaurant, include:
        - Name
        - Cuisine type
        - 2-3 must-try dishes with prices
        - Cost for 2 people in ₹
        
        ## 3. Activities for {interests}
        List 5 specific activities matching the interests with:
        - Activity name
        - Cost in ₹
        - Duration
        
        ## 4. Events During Visit
        List any festivals/events happening during {date_from} to {date_to}:
        - Event name
        - Date
        - Location
        - Cost (if any)
        
        ## 5. Hidden Gems
        List 3 lesser-known places with:
        - Name
        - Why it's special
        - Cost (if any)
        
        **IMPORTANT:** Write ALL 5 sections with specific names and prices. Do NOT just search!
        """,
        expected_output="""A complete markdown guide with:
        - 5 attractions with names, descriptions, and entry fees
        - 5 restaurants with names, dishes, and costs
        - 5 activities matching user interests
        - Events during travel dates
        - 3 hidden gems
        All prices must be in ₹ (Indian Rupees)""",
        agent=agent,
        output_file='guide_report.md',
    )

# ============================================================================
# TASK 3: Complete Itinerary Planning (SIMPLIFIED)
# ============================================================================
def planner_task(context, agent, destination_city, interests, date_from, date_to, num_adults=2, num_children=0):
    total_persons = num_adults + num_children
    
    return Task(
        description=f"""
        **CRITICAL: After 2 web searches, STOP searching and write your complete itinerary!**
        
        Create a day-by-day itinerary for {destination_city} from {date_from} to {date_to}.
        Travelers: {num_adults} adults + {num_children} children = {total_persons} total persons.
        Interests: {interests}
        
        **YOUR TASK (Complete in 2 steps):**
        1. Quick search if needed (1-2 searches max)
        2. **STOP SEARCHING** and write your complete itinerary below
        
        **Write a complete itinerary with these 5 sections:**
        
        ## 1. City Introduction (3 paragraphs)
        
        **Paragraph 1 - Overview (3-4 sentences):**
        What makes {destination_city} special, key highlights, why travelers visit.
        
        **Paragraph 2 - Culture & Food (3-4 sentences):**
        Cultural heritage, signature dishes, food scene, dining costs.
        
        **Paragraph 3 - Best for {interests} (3-4 sentences):**
        Top activities matching {interests}, best areas to explore, unique experiences.
        
        ## 2. Day-by-Day Plan
        For EACH day from {date_from} to {date_to}, provide:
        
        **Day X: [Theme]**
        - **Morning:** Activity name, duration, cost ₹X
        - **Lunch:** Restaurant name, dishes, cost ₹X for {total_persons}
        - **Afternoon:** Activity name, duration, cost ₹X
        - **Dinner:** Restaurant name, dishes, cost ₹X for {total_persons}
        - **Evening/Night:** Activity (if nightlife interest), cost ₹X
        - **Daily Total:** ₹X per person
        
        ## 3. Budget Breakdown
        **Transportation:**
        - Flights: ₹X × {total_persons} = ₹X
        - Local transport: ₹X/day × X days = ₹X
        - Subtotal: ₹X
        
        **Accommodation:**
        - Hotel: [Name]
        - ₹X/night × X nights = ₹X
        
        **Food:**
        - ₹X/day × X days = ₹X
        
        **Activities:**
        - Total: ₹X
        
        **TOTAL FOR {total_persons} PEOPLE: ₹X**
        **Per Person: ₹X**
        
        ## 4. Practical Tips
        **Transport:** Best option, cost, apps to use
        **Safety:** Safety level, emergency numbers
        **Money-Saving:** 3 budget tips
        **Customs:** 2-3 important local customs
        
        ## 5. Packing List
        **Clothing:** (based on weather)
        **Essentials:** Passport, visa, insurance, ₹X cash
        **Electronics:** Charger, adapter (plug type for {destination_city})
        **Other:** 3-4 important items
        
        **IMPORTANT:** Write ALL 5 sections with specific details. Include ALL days from {date_from} to {date_to}. Do NOT just search!
        """,
        expected_output=f"""A complete markdown itinerary with:
        - 3 paragraphs city introduction
        - Day-by-day plan for EVERY day with specific activities, restaurants, and costs
        - Complete budget breakdown for {total_persons} person(s)
        - Practical tips (transport, safety, money-saving, customs)
        - Packing list
        All prices must be in ₹ (Indian Rupees) and calculated for {total_persons} person(s)""",
        agent=agent,
        context=context,
        output_file='final_itinerary.md',
    )

# ============================================================================
# TASK 4: Booking & Transport Research
# ============================================================================
def booking_task(agent, category, from_location, to_location, date, details):
    return Task(
        description=f"""
        **CRITICAL: Search for {category} options from {from_location} to {to_location} on {date}.**
        Details: {details}
        
        **YOUR TASK (Complete in 2 steps):**
        1. Search for available {category} options with prices (1-2 searches)
        2. **STOP SEARCHING** and write your complete report below in the specified format.
        
        **Write a complete report with these sections:**
        
        ## 1. Top 3 {category} Options
        For each option, provide:
        - Name (Airline/Train/Bus/Hotel)
        - Departure/Arrival Time (if applicable)
        - Duration
        - Price in ₹
        - Rating/Reviews (if available)
        - Booking Link (if found, otherwise mention "Check official website")
        
        ## 2. Recommendation
        - Best option for budget
        - Best option for comfort/speed
        
        ## 3. Practical Tips for {category}
        - Booking advice
        - What to expect
        
        **IMPORTANT:** Be specific with names and prices in Indian Rupees (₹).
        """,
        expected_output=f"""A complete markdown report with 3 top {category} options, prices, and recommendations.""",
        agent=agent,
        output_file=f'{category.lower().replace(" ", "_")}_report.md',
    )
