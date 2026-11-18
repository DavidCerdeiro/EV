from app.prompts.system import compose_prompt

def build_general_prompt(user_name: str) -> str:
    return compose_prompt(
        user_name,
        "Respondes a preguntas y peticiones generales de los usuarios. Mantén una conversación fluida y concisa."
    )