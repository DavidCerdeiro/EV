from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

from app.core.llm import get_assistant_llm
from app.prompts.weather_prompt import build_weather_prompt
from app.tools.weather_tools import WEATHER_TOOLS

weather_agent = create_agent(
    model=get_assistant_llm(),
    tools=WEATHER_TOOLS
)

def weather_node(state: dict):
    name = state.get("user_name", "Usuario")
    
    dinamic_prompt = build_weather_prompt(name)
    system_msg = SystemMessage(content=dinamic_prompt)
    
    messages_for_agent = [system_msg] + state["messages"]
    
    response = weather_agent.invoke({"messages": messages_for_agent})
    
    nuevo_mensaje = response["messages"][-1]
    
    return {"messages": [nuevo_mensaje]}