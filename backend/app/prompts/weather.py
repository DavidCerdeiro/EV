from app.prompts.system import compose_prompt


WEATHER_ROLE = (
    "Tu tema es el tiempo meteorológico. Usa siempre las herramientas, "
    "nunca respondas de memoria. Si el usuario no menciona un lugar, no "
    "preguntes: usa el lugar por defecto. Para mañana usa el día uno, "
    "para pasado mañana el día dos. Responde solo con lo que se pregunta: "
    "si piden la temperatura, no añadas el viento."
)


def build_weather_prompt() -> str:
    return compose_prompt(WEATHER_ROLE)