import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.rate_limiters import InMemoryRateLimiter


load_dotenv()


# ============================================================
# 1. INITIALIZE A MODEL
# ============================================================

model = init_chat_model(
    "google_genai:gemini-3.7-flash",
    temperature=0.7,
)

print("\nMODEL:")
print(model)


# ============================================================
# 2. INVOKE
# ============================================================

def demo_invoke():

    print("\n========== INVOKE ==========")

    response = model.invoke(
        "Explain what an AI agent is in 3 sentences."
    )

    print(response.content)


# ============================================================
# 3. STREAM
# ============================================================

def demo_stream():

    print("\n========== STREAM ==========")

    for chunk in model.stream(
        "Explain LangChain models in simple terms."
    ):
        print(chunk.content, end="", flush=True)

    print()


# ============================================================
# 4. BATCH
# ============================================================

def demo_batch():

    print("\n========== BATCH ==========")

    questions = [
        "What is an AI agent?",
        "What is tool calling?",
        "What is structured output?",
    ]

    responses = model.batch(questions)

    for question, response in zip(questions, responses):

        print("\nQUESTION:", question)
        print("ANSWER:", response.content)


# ============================================================
# 5. MODEL PARAMETERS
# ============================================================

def demo_parameters():

    print("\n========== PARAMETERS ==========")

    creative_model = init_chat_model(
        "google_genai:gemini-3.7-flash",
        temperature=1.0,
        max_tokens=100,
        timeout=30,
        max_retries=2,
    )

    response = creative_model.invoke(
        "Give me a creative name for an AI startup."
    )

    print(response.content)


# ============================================================
# 6. TOOL CALLING
# ============================================================

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    return f"The weather in {city} is sunny and 28°C."


def demo_tool_calling():

    print("\n========== TOOL CALLING ==========")

    model_with_tools = model.bind_tools(
        [get_weather]
    )

    response = model_with_tools.invoke(
        "What is the weather in Bangalore?"
    )

    print("\nMODEL RESPONSE:")
    print(response)

    print("\nTOOL CALLS:")
    print(response.tool_calls)

    # Execute the tool manually.
    for tool_call in response.tool_calls:

        if tool_call["name"] == "get_weather":

            result = get_weather.invoke(
                tool_call["args"]
            )

            print("\nTOOL RESULT:")
            print(result)


# ============================================================
# 7. STRUCTURED OUTPUT
# ============================================================

class Movie(BaseModel):
    title: str = Field(
        description="The movie title"
    )

    year: int = Field(
        description="The release year"
    )

    genre: str = Field(
        description="The movie genre"
    )

    rating: float = Field(
        description="The movie rating out of 10"
    )


def demo_structured_output():

    print("\n========== STRUCTURED OUTPUT ==========")

    structured_model = model.with_structured_output(
        Movie
    )

    response = structured_model.invoke(
        """
        Give me information about the movie Inception.
        Include its title, release year, genre and rating.
        """
    )

    print(response)

    print("\nTITLE:", response.title)
    print("YEAR:", response.year)
    print("GENRE:", response.genre)
    print("RATING:", response.rating)


# ============================================================
# 8. TOKEN USAGE
# ============================================================

def demo_token_usage():

    print("\n========== TOKEN USAGE ==========")

    response = model.invoke(
        "Explain machine learning in 100 words."
    )

    print("\nRESPONSE:")
    print(response.content)

    print("\nUSAGE:")
    print(response.usage_metadata)


# ============================================================
# 9. MODEL EXCEPTIONS
# ============================================================

def demo_exceptions():

    print("\n========== MODEL EXCEPTIONS ==========")

    try:

        response = model.invoke(
            "Explain artificial intelligence."
        )

        print(response.content)

    except Exception as e:

        print("\nMODEL ERROR:")
        print(type(e).__name__)
        print(e)


# ============================================================
# 10. RATE LIMITING
# ============================================================

def demo_rate_limiting():

    print("\n========== RATE LIMITING ==========")

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.5,
        check_every_n_seconds=0.1,
        max_bucket_size=1,
    )

    limited_model = init_chat_model(
        "google_genai:gemini-3.7-flash",
        temperature=0,
        rate_limiter=rate_limiter,
    )

    response = limited_model.invoke(
        "What is Python?"
    )

    print(response.content)


# ============================================================
# 11. CONFIGURABLE MODEL
# ============================================================

def demo_configurable_model():

    print("\n========== CONFIGURABLE MODEL ==========")

    configurable_model = init_chat_model(
        "google_genai:gemini-3.7-flash",
        temperature=0,
        configurable_fields=(
            "model",
            "model_provider",
            "temperature",
        ),
    )

    response = configurable_model.invoke(
        "What is LangChain?",
        config={
            "configurable": {
                "model": "gemini-3.7-flash",
                "model_provider": "google_genai",
                "temperature": 0.2,
            }
        },
    )

    print(response.content)


# ============================================================
# 12. DYNAMIC MODEL SELECTION
# ============================================================

def choose_model(task: str):

    if task == "simple":

        return init_chat_model(
            "google_genai:gemini-3.7-flash",
            temperature=0,
        )

    elif task == "creative":

        return init_chat_model(
            "google_genai:gemini-3.7-flash",
            temperature=1.0,
        )

    else:

        return model


def demo_dynamic_model():

    print("\n========== DYNAMIC MODEL SELECTION ==========")

    task = "creative"

    selected_model = choose_model(task)

    response = selected_model.invoke(
        "Give me an interesting name for an AI project."
    )

    print(response.content)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    demo_invoke()

    demo_stream()

    demo_batch()

    demo_parameters()

    demo_tool_calling()

    demo_structured_output()

    demo_token_usage()

    demo_exceptions()

    demo_rate_limiting()

    demo_configurable_model()

    demo_dynamic_model()