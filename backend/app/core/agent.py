from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import MemorySaver

from app.core.llm import get_assistant_llm
from app.prompts.weather import build_weather_prompt
from app.tools.weather import WEATHER_TOOLS


@before_model
def trim_messages(state, runtime):
    """Mantiene solo los últimos 12 mensajes."""
    messages = state["messages"]
    if len(messages) <= 12:
        return None  # sin cambios

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *messages[-12:],
        ]
    }


weather_agent = create_agent(
    model=get_assistant_llm(),
    tools=WEATHER_TOOLS,
    system_prompt=build_weather_prompt(),
    middleware=[trim_messages],
    checkpointer=MemorySaver(),
)