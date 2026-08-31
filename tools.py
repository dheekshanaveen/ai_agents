from langchain.tools import tool
import requests


@tool
def calculator(a: float, b: float) -> float:
    """Multiply two numbers."""
    
    print("\n[CALCULATOR TOOL CALLED]")
    
    return a * b


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    print("\n[WEATHER TOOL CALLED]")
    print("City:", city)

    url = f"https://wttr.in/{city}?format=3"

    response = requests.get(url)

    print("API RESULT:", response.text)

    return response.text