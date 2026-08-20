from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel

load_dotenv()


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


class CalculationResult(BaseModel):
    operation: str
    a: float
    b: float
    result: float


agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=[add_numbers, multiply_numbers],
    system_prompt="You are a helpful assistant.",
    response_format=CalculationResult,
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

    result = response["structured_response"]

    print("Operation:", result.operation)
    print("A:", result.a)
    print("B:", result.b)
    print("Result:", result.result)