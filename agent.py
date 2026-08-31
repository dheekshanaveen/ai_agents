from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langchain.tools import tool
import requests
from pydantic import BaseModel, Field
from langchain_core.utils.uuid import uuid7
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()



@before_model
def my_middleware(state, runtime):
    print("\n[MIDDLEWARE] Before Gemini is called")
    print("[MIDDLEWARE] User message:", state["messages"][-1].content)


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    print("\nWEATHER TOOL WAS CALLED")
    print("City:", city)

    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)

    print("API RESULT:", response.text)

    return response.text


backend = StateBackend()


agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_weather],
    system_prompt="""
You are a weather assistant.

IMPORTANT:
YOU HAVE ACCESS TO TOOLS USE THEM WHEN NEEDED.
""",
    middleware=[
        my_middleware,
        FilesystemMiddleware(backend=backend)
    ],
)

while True:
    user_input = input("\nWHATS THE MATTER GORGEOUS: ")

    if user_input.lower() == "exit":
        break

    print("\n--- STREAMING ---")

    for chunk in agent.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config,
        stream_mode="updates"
    ):
        print("\nCHUNK:")
        print(chunk)
        if "model" in chunk:
            message = chunk["model"]["messages"][0]

            if message.content:
                if isinstance(message.content, list):
                    for item in message.content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            print(item["text"], end="", flush=True)
                else:
                    print(message.content, end="", flush=True)

    print()
