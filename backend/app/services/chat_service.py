from app.core.agent import weather_agent
from app.schemas.chat_schema import ChatResponse
from app.utils.tts_sanitizer import sanitize_for_tts

async def response_to_user(user_message: str) -> ChatResponse:
    config = {"configurable": {"thread_id": "ev_local_session"}}
    
    result = await weather_agent.ainvoke({"messages": [("human", user_message)]}, config=config)
    raw_answer = result["messages"][-1].content
    return ChatResponse(model_response=sanitize_for_tts(raw_answer))