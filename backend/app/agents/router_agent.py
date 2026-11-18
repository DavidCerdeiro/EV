from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.messages import SystemMessage

from app.core.llm import get_router_llm

class Route(BaseModel):
    next_agent: Literal["weather_agent", "general_agent"] = Field(
        description="El agente encargado de resolver la petición del usuario."
    )

async def router_agent(state: dict) -> Route:
    """
    Determina qué agente debe manejar la petición del usuario.
    """
    system_prompt = SystemMessage(content="""
    Eres el ENRUTADOR PRINCIPAL del asistente de voz E.V.
    REGLA CRÍTICA ABSOLUTA: NO respondas a las preguntas del usuario. NUNCA generes texto conversacional.
    Tu ÚNICA tarea es clasificar la intención del último mensaje del usuario y devolver EXACTAMENTE UNO de estos valores:
    - 'weather_agent': Consultas sobre el clima, temperatura, pronósticos.
    - 'general_agent': Saludos, chistes, preguntas generales, o cualquier cosa que no encaje en los anteriores.
    """)

    messages = [system_prompt] + state["messages"]
    structured_llm = get_router_llm().with_structured_output(Route)
    
    response = await structured_llm.ainvoke(messages)

    return response.next_agent