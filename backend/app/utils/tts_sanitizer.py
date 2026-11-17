import re
from num2words import num2words

_EMOJI = re.compile("[\U00010000-\U0010ffff\u2600-\u27bf]")
_MARKDOWN = re.compile(r"[*#_`>~\[\]]")


def _number_to_words(match: re.Match) -> str:
    text = match.group(0).replace(",", ".")
    number = float(text) if "." in text else int(text)
    return num2words(number, lang="es")


def sanitize_for_tts(text: str) -> str:
    text = _EMOJI.sub("", text)                                    # quita emojis
    text = _MARKDOWN.sub("", text)                                 # quita símbolos de Markdown
    text = text.replace("°C", " grados").replace("°", " grados")   # temperaturas
    text = re.sub(r"(\d+(?:[.,]\d+)?)\s*%", r"\1 por ciento", text)  # porcentajes
    text = re.sub(r"\d+(?:[.,]\d+)?", _number_to_words, text)      # cifras -> palabras
    return re.sub(r"\s+", " ", text).strip()                       # espacios sobrantes