from fastapi import FastAPI, HTTPException
import re

app = FastAPI()

# Load prohibited words from file
def load_prohibited_words(filename="prohibited_word.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return set(word.strip().lower() for word in file.readlines())
    except FileNotFoundError:
        return set()

prohibited_words = load_prohibited_words()

# Function to moderate user input
def treat_input(user_input: str):
    if not user_input:
        return ""
    
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, prohibited_words)) + r")\b", re.IGNORECASE)
    moderated_text = pattern.sub("***", user_input)
    
    return moderated_text

@app.post("/moderate")
def moderate_text(params: dict):
    text_input = params.get("text_input")
    if not text_input:
        raise HTTPException(status_code=400, detail="text_input is required")
    
    treated_response = treat_input(text_input)
    return {"original": text_input, "moderated": treated_response}

# Run with: fastapi dev app.py
# Access with: http://localhost:8000/docs
