from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7


memory = InMemorySaver()

config = {
    "configurable": {
        "thread_id": str(uuid7())
    }
}