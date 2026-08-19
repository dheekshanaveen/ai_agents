from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    system_prompt="You are a helpful assistant.",
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is artificial intelligence?"
            }
        ]
    }
)

print(response["messages"][-1].content[0]["text"])