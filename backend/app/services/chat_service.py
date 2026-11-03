from app.schemas.chat_schema import ChatResponse
from app.core.llm import get_router_llm, get_assistant_llm, get_document_llm

# This function takes a user message as input, processes it through the assistant LLM, and returns a structured response.
def response_to_user(user_message: str) -> ChatResponse:
    system_prompt = (
        "Eres E.V., una interfaz de voz inteligente, directa y concisa. "
        "Tus respuestas serán procesadas por un sintetizador de voz, por lo que debes cumplir estrictamente estas reglas de formato auditivo:\n"
        "1. SIN FORMATO VISUAL: Prohibido usar Markdown, asteriscos, almohadillas, viñetas o caracteres especiales. Tu salida debe ser texto plano puro.\n"
        "2. CERO EMOJIS: No incluyas emojis bajo ninguna circunstancia.\n"
        "3. NÚMEROS A TEXTO: Escribe todas las cifras, años, fechas y símbolos matemáticos con palabras (ejemplo: 'dos mil veintiséis' en lugar de '2026', 'ochenta por ciento' en lugar de '80%').\n"
        "4. ABREVIATURAS: Escribe las palabras completas (ejemplo: 'por ejemplo' en lugar de 'ej.', 'doctor' en lugar de 'Dr.').\n"
        "5. RITMO Y CADENCIA: Usa comas y puntos estratégicamente para forzar pausas naturales en la respiración del lector. Evita párrafos largos."
    )
    
    messages = [
        ("system", system_prompt),
        ("human", user_message)
    ]
    
    ai_message = get_assistant_llm().invoke(messages)

    chat_response = ChatResponse(model_response=ai_message.content)

    return chat_response
