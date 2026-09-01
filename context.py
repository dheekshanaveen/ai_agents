from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.6-flash",

    system_prompt="""
You are a helpful coding assistant.

The user is learning Python and AI agents.
Keep explanations simple.
"""
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Explain what an API is."
            }
        ]
    }
)

print(result["messages"][-1].content)