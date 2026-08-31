from dotenv import load_dotenv
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

load_dotenv()


# ============================================
# FILE ENVIRONMENT
# ============================================

backend = StateBackend()


# ============================================
# AGENT
# ============================================

agent = create_agent(
    model="google_genai:gemini-3.6-flash",

    system_prompt="""
You are a helpful assistant.

You have access to a filesystem.
Use the filesystem tools when you need to
create, read, write, or modify files.
you should use tools when you need to perform actions that require access to the filesystem.
""",

    middleware=[
        FilesystemMiddleware(backend=backend)
    ],
)


# ============================================
# CHAT LOOP
# ============================================

while True:

    user_input = input("\nWHAT CAN I DO FOR YOU BEAUTIFUL: ")

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

    print("\nAGENT:")
    print(response["messages"][-1].content)