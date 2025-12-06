from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

try:
    llm = LLM(model="gemini/gemini-2.0-flash")
    agent = Agent(role='Test', goal='Test', backstory='Test', llm=llm)
    task = Task(description='Say hi', agent=agent, expected_output='hi')
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    print(f"Type of result: {type(result)}")
    print(f"Result content: {result}")
    if hasattr(result, 'raw'):
        print(f"Result raw: {result.raw}")
except Exception as e:
    print(f"Error: {e}")
