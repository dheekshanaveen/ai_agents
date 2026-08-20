from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=[add_numbers, multiply_numbers],
    system_prompt="You are a helpful assistant.",
)


while True:
    user_input = input("\nYou: ")

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