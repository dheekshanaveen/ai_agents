from dotenv import load_dotenv
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

load_dotenv()


# 1. Create the environment
backend = StateBackend()


# 2. Create the agent
agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    name="FileAgent",
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


# 3. Ask the agent to create and then edit a file
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """
Create a file called dhee.txt

and write everything you know aabout me in it, like what i am learning and doing. 

Finally, read the file and return its final contents.
"""
            }
        ]
    }
)


# 4. Print the final response
print("\nAGENT RESPONSE:")
print(result["messages"][-1].content)