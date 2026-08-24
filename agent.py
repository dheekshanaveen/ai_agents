from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
import requests
from pydantic import BaseModel, Field
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

class WeatherResponse(BaseModel):
    city: str = Field(description="Name of the city")
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Current weather condition")


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    url = f"https://wttr.in/{city}?format=3"

    response = requests.get(url)

    return response.text


agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_weather],
    system_prompt="You are a helpful weather assistant.",
    response_format=WeatherResponse,
    checkpointer=InMemorySaver(),
)

config = {
    "configurable": {
        "thread_id": str(uuid7())
    }
} 

while True:
    user_input = input("\nHow CAN I HELP YOU GORGEOUS: ")

    if user_input.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        print("Agent:", content[0]["text"])
    else:
        print("Agent:", content)

