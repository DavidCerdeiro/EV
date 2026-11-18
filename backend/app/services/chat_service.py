from sqlalchemy.orm import Session
import groq

from app.schemas.chat_schema import ChatResponse
from app.utils.tts_sanitizer import sanitize_for_tts
from app.agents.graph import ev_graph
from app.models.user import User

async def response_to_user(user_message: str, db: Session) -> ChatResponse:
    db_user = db.query(User).first()

    user_name = db_user.name if db_user else "Usuario"

    config = {"configurable": {"thread_id": "ev_local_session"}}
    try:
        result = await ev_graph.ainvoke(
            {"messages": [("human", user_message)], "user_name": user_name}, 
            config=config
        )
        
        raw_answer = result["messages"][-1].content

    except groq.BadRequestError as e:
        # Si el modelo de 20B alucina y falla la validación de Groq
        print(f"Groq Bad Request Error: {e}")
        raw_answer = "Lo siento, me he liado procesando eso. ¿Podrías repetírmelo de otra forma?"
        
    except Exception as e:
        # Fallback de seguridad global (caída de red, error de BD, etc.)
        print(f"Error general en LangGraph: {e}")
        raw_answer = "Ha ocurrido un error en mi sistema. Dame un segundo e inténtalo de nuevo."
    
    return ChatResponse(model_response=sanitize_for_tts(raw_answer))