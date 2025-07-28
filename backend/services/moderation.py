"""
Service functions for moderating user input, both manually (using a word filter) and with AI (using LangChain/OpenAI).
"""
import re
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Manual moderation using regex and word list
def treat_input(user_input: str, prohibited_words: set) -> str:
    """
    Replace prohibited words in the input text with '***'.
    """
    if not user_input:
        return ""
    if not prohibited_words:
        return user_input
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, prohibited_words)) + r")\b", re.IGNORECASE)
    moderated_text = pattern.sub("***", user_input)
    return moderated_text

# Professional, context-aware moderator prompt
def get_moderator_prompt() -> str:
    """
    Returns a professional prompt for the AI moderator.
    """
    return (
        "You are a professional content moderator. "
        "Your job is to review user-submitted text for any offensive language, hate speech, personal information, or policy violations. "
        "If you find any such content, replace only the problematic words or phrases with '***'. "
        "Do not alter the meaning of the rest of the text. "
        "If the text is clean, return it unchanged. "
        "Here is the text to moderate: {input}"
    )

# LangChain-based AI moderation
def ai_treat_input(user_input: str) -> str:
    """
    Use a language model (via LangChain) to moderate the input text.
    """
    if not user_input:
        return ""
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
        prompt = ChatPromptTemplate.from_template(get_moderator_prompt())
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"input": user_input})
        return result.strip()
    except Exception as e:
        return f"[AI moderation failed: {str(e)}] {user_input}" 