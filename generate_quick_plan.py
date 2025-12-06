import os
import time
from dotenv import load_dotenv
from crewai import Crew, Process, LLM
from TravelAgents import location_expert, guide_expert, planner_expert
from TravelTasks_LEGACY import location_task_legacy, guide_task_legacy, planner_task_legacy

load_dotenv()

def generate_plan():
    print("🚀 Generating Sample Trip Plan (to verify format)...")
    
    # Configuration
    from_city = "New York"
    destination_city = "Paris"
    date_from = "2025-05-10"
    date_to = "2025-05-11" # Short trip for speed
    interests = "Food, Landmarks"
    num_adults = 1
    
    # LLM Setup - Use Ollama
    print("🐌 Using Ollama (Groq was limited)...")
    llm = LLM(
        model="ollama/llama3.2",
        base_url="http://localhost:11434"
    )
    
    # Assign LLM
    location_expert.llm = llm
    guide_expert.llm = llm
    planner_expert.llm = llm
    
    # Tasks
    task1 = location_task_legacy(location_expert, from_city, destination_city, date_from, date_to, num_adults)
    task2 = guide_task_legacy(guide_expert, destination_city, interests, date_from, date_to)
    task3 = planner_task_legacy([task1, task2], planner_expert, destination_city, interests, date_from, date_to, num_adults)
    
    crew = Crew(
        agents=[location_expert, guide_expert, planner_expert],
        tasks=[task1, task2, task3],
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        output_file = "sample_paris_plan.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(result))
        print(f"\n✅ Plan Generated Successfully! Saved to {output_file}")
    except Exception as e:
        print(f"\n❌ Generation Failed: {e}")

if __name__ == "__main__":
    generate_plan()
