from dotenv import load_dotenv
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from langchain.chat_models import init_chat_model
load_dotenv()


# 1. Create the environment/backend
backend = StateBackend()

model = init_chat_model(
    "google/gemini-3.6-flash",
    model_provider="openrouter"
)
# 2. Create the agent
agent = create_agent(
    model="google/gemini-3.6-flash",
    model_provider="openrouter",

    system_prompt="""
You are an assistant that can work with files.

You have access to a filesystem environment.
Use the filesystem tools whenever the user asks you to
create, read, write, edit, or list files.
""",

    middleware=[
        FilesystemMiddleware(backend=backend)
    ],
)


# 3. Run the agent
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                 "content": "create a file called notes.txt and write 'This is my first file stored in the environment.' into it. Then read the file back and return its content."
            }
        ]
    }
)


# 4. Print the final response
print("\nAGENT RESPONSE:")
print(result["messages"][-1].content)