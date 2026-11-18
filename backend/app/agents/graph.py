from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import RemoveMessage
from langgraph.checkpoint.memory import MemorySaver

from app.agents.router_agent import router_agent
from app.agents.general_agent import general_node
from app.agents.weather_agent import weather_node


def trim_messages_node(state: dict):
    """Mantiene solo los últimos 12 mensajes en el estado global."""
    messages = state["messages"]
    
    if len(messages) <= 12:
        return {"messages": []} # No hay cambios
    
    # Identificamos los mensajes sobrantes (todos excepto los últimos 12)
    messages_to_remove = messages[:-12]
    
    # Devolvemos las instrucciones de borrado para el reducer
    return {
        "messages": [RemoveMessage(id=m.id) for m in messages_to_remove]
    }

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_name: str

workflow = StateGraph(AgentState)

workflow.add_node("trim_messages", trim_messages_node)
workflow.add_node("weather_agent", weather_node)
workflow.add_node("general_agent", general_node)

workflow.add_edge(START, "trim_messages")

workflow.add_conditional_edges(
    "trim_messages",
    router_agent,
    {
        "weather_agent": "weather_agent",
        "general_agent": "general_agent",
    }
)

workflow.add_edge("weather_agent", END)
workflow.add_edge("general_agent", END)

memory = MemorySaver()
ev_graph = workflow.compile(checkpointer=memory)