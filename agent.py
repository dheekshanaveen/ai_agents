from langchain.agents import create_agent

agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[],
    system_prompt="You are a helpful assistant.",
)

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What is artificial intelligence?"}
        ]
    }
)

print(response["messages"][-1].content)