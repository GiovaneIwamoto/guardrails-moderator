import re
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Request body model
class TextInput(BaseModel):
    text_input: str


# Create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI
app = FastAPI()

# Load prohibited words from a file
def load_prohibited_words(filename="template/word_filter.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return set(word.strip().lower() for word in file.readlines())
    except FileNotFoundError:
        return set()

prohibited_words = load_prohibited_words()

# Manual moderation using regex and word list
def treat_input(user_input: str):
    if not user_input:
        return ""

    pattern = re.compile(r"\b(" + "|".join(map(re.escape, prohibited_words)) + r")\b", re.IGNORECASE)
    moderated_text = pattern.sub("***", user_input)

    return moderated_text


# AI-powered moderation using OpenAI API
def ai_treat_input(user_input: str):
    if not user_input:
        return ""

    prompt = f"Replace any offensive words or personal info in this sentence with '***':\n\n{user_input}"

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a content moderator."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# Endpoint for manual moderation
@app.post("/manualmoderate")
def manual_moderate_text(params: TextInput):
    text_input = params.text_input

    if not text_input:
        raise HTTPException(status_code=400, detail="text_input is required")

    treated_response = treat_input(text_input)

    return {
        "original": text_input,
        "moderated": treated_response
    }


# Endpoint for AI moderation
@app.post("/aimoderate")
def ai_moderate_text(params: TextInput):
    text_input = params.text_input

    if not text_input:
        raise HTTPException(status_code=400, detail="text_input is required")

    try:
        treated_response = ai_treat_input(text_input)
    except Exception as e:
        treated_response = f"AI moderation failed: {str(e)}"

    return {
        "original": text_input,
        "moderated": treated_response
    }
