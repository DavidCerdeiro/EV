import os
from langchain_groq import ChatGroq

def get_router_llm() -> ChatGroq:
    """
    GPT OSS (120B): Principal model for routing and classification tasks.
    """
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.1,
        max_tokens=1024
    )

def get_assistant_llm() -> ChatGroq:
    """
    GPT OSS (20B): Fast model for general assistant tasks, optimized for speed and efficiency.
    """
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.5,
        max_tokens=1024
    )

def get_document_llm() -> ChatGroq:
    """
    GPT OSS (120B): Model for document processing tasks, capable of handling larger contexts and complex queries.
    """
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        max_tokens=4096
    )