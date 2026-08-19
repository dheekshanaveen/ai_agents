# AI Agents with LangChain

A beginner-friendly project for learning how to build AI agents using **LangChain, Google Gemini, and Python**.

The project follows the current LangChain documentation and builds the agent step by step instead of using a pre-built framework without understanding what is happening underneath.

## What This Project Does

The first version of the project creates a simple AI agent that:

* Uses **LangChain** to create and manage the agent.
* Uses **Google Gemini** as the language model.
* Accepts a user question.
* Sends the question to Gemini through LangChain.
* Returns the model's response.

Later, the agent can be extended with tools so that it can perform actions instead of only generating text.

## Tech Stack

* **Python 3.13.7**
* **LangChain**
* **Google Gemini**
* **langchain-google-genai**
* **LangGraph** — used internally by LangChain's agent system

## Project Structure

```text
ai_agents/
│
├── agent.py
└── README.md
```

### `agent.py`

This is the main Python file. It creates the LangChain agent, sends a question to the model, and prints the response.

## Setup

### 1. Check Python

This project requires Python 3.10 or higher.

The current development environment uses:

```text
Python 3.13.7
```

Check your version with:

```powershell
python --version
```

### 2. Install LangChain

Install LangChain using pip:

```powershell
pip install -U langchain
```

### 3. Install Google Gemini support

Install the Google GenAI integration:

```powershell
pip install -U "langchain[google-genai]"
```

This allows LangChain to communicate with Google's Gemini models.

## API Key Setup

The project uses a Gemini API key to communicate with Google's API.

Create an API key through **Google AI Studio**.

Do not put the API key directly inside `agent.py`.

For PowerShell, set the key in the current terminal session:

```powershell
$env:GOOGLE_API_KEY="YOUR_API_KEY"
```

Check that Python can see the variable:

```powershell
python -c "import os; print('API key found:', bool(os.getenv('GOOGLE_API_KEY')))"
```

Expected output:

```text
API key found: True
```

Never upload your API key to GitHub or share it publicly.

## Current Agent

The basic agent looks like this:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[],
    system_prompt="You are a helpful assistant.",
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is artificial intelligence?"
            }
        ]
    }
)

print(response["messages"][-1].content)
```

## How It Works

The important part is:

```python
agent = create_agent(...)
```

`create_agent()` creates the agent using the model, tools, and instructions we provide.

### Model

```python
model="google_genai:gemini-2.5-flash"
```

This tells LangChain to use Google's Gemini 2.5 Flash model through the Google GenAI integration.

The `google_genai:` part explicitly identifies the model provider.

### Tools

```python
tools=[]
```

Currently, the agent has no tools.

This means it can answer questions using the language model, but it cannot independently perform actions such as checking the weather, searching a database, or calling an API.

Tools will be added as the project develops.

### System Prompt

```python
system_prompt="You are a helpful assistant."
```

This gives the agent its basic behavior and instructions.

### Invoke

```python
agent.invoke(...)
```

This sends the user's message to the agent and starts the agent's execution.

The response contains a list of messages, so we retrieve the final message with:

```python
response["messages"][-1].content
```

## Running the Project

From the project directory:

```powershell
python agent.py
```

If everything is configured correctly, the terminal should print Gemini's response.

## Important Troubleshooting

### `API key not valid`

If you see:

```text
400 INVALID_ARGUMENT
API key not valid. Please pass a valid API key.
```

the API key exists as an environment variable, but Google is rejecting its value.

Check that:

* The key was copied correctly.
* The key was created in Google AI Studio.
* The key has not been deleted or revoked.
* There are no unwanted characters or spaces.
* The terminal contains the correct key.

You can check whether a key exists without printing the actual key:

```powershell
python -c "import os; print('API key found:', bool(os.getenv('GOOGLE_API_KEY')))"
```

### `langchain_google_vertexai` error

If LangChain tries to use:

```text
langchain-google-vertexai
```

when you intended to use Google AI Studio, make the provider explicit:

```python
model="google_genai:gemini-2.5-flash"
```

We are using the Google GenAI integration rather than Vertex AI for this project.

### AFC warning

You may see a message similar to:

```text
Direct use of automatic function calling (AFC) ...
```

This is not necessarily the cause of an API failure. It is related to how Google's newer SDK handles automatic function calling.

For the current basic agent, the important thing is whether the Gemini API request itself succeeds.

## Learning Path

This project is being built progressively.

### Stage 1 — Basic Agent

```text
User
 ↓
LangChain Agent
 ↓
Gemini
 ↓
Response
```

### Stage 2 — Add Tools

The agent will be given functions it can use.

For example:

```text
User
 ↓
Agent
 ↓
Does it need a tool?
 ↓
 ├── No → Gemini → Response
 │
 └── Yes → Tool → Result → Gemini → Response
```

### Stage 3 — Build a Useful Agent

Once the basic concepts are understood, the project can be extended with real tools such as:

* Weather APIs
* Web search
* Calculator
* Database queries
* Custom Python functions
* External APIs

The goal is not just to copy an agent from a tutorial, but to understand **why each component is needed and how the pieces communicate with each other**.

## Current Status

* [x] Python environment set up
* [x] LangChain installed
* [x] Google GenAI integration installed
* [x] Gemini API key configured
* [x] Basic `create_agent()` structure created
* [ ] Successfully complete Gemini API test
* [ ] Add the first custom tool
* [ ] Understand tool calling
* [ ] Build a practical agent
* [ ] Add multiple tools
* [ ] Improve the agent's reliability and error handling

## Useful Links

* LangChain documentation: https://docs.langchain.com/oss/python/langchain/overview
* Google AI Studio: https://aistudio.google.com/
* Gemini API documentation: https://ai.google.dev/gemini-api/docs

## Goal of the Project

The main goal is to learn **how AI agents actually work**, starting from a simple LangChain agent and gradually adding tools, decision-making, APIs, and more advanced capabilities.

The project will be kept simple at each stage so that the underlying concepts are understood before moving to the next level.
