from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

load_dotenv()

try:
    llm = LLM(model="gemini/gemini-2.0-flash")
    
    agent = Agent(
        role='Test Agent',
        goal='Say hello',
        backstory='A friendly agent',
        llm=llm,
        verbose=True
    )

    task = Task(
        description='Say hello to the world',
        agent=agent,
        expected_output='A hello message'
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    print("Result:", result)

except Exception as e:
    print(f"Error: {e}")
