# This is the CORRECTED tier loop section (lines 821-920 approximately)
# Replace the corrupted section in ratnesh_app_ULTIMATE.py with this

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
                    st.info(f"\U0001f680 **[TIER {tier_num}]** Trying {tier_name} {tier_config['emoji']} (~{tier_config['time']})...")
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
