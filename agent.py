from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
import requests

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    url = f"https://wttr.in/{city}?format=3"

    response = requests.get(url)

    return response.text


agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant. Use the weather tool when the user asks about weather.",
)


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
        }
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        print("Agent:", content[0]["text"])
    else:
        print("Agent:", content)