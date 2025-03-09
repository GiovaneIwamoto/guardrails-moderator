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

#function to moderate user input with ai
def ai_treat_input(user_input: str):
    if not user_input:
        return ""
    
    #request to ai : "replace the swear words and personal data present in the sentence with "***" ..."
    #save the response as ai_response
    moderated_text = ("ai_response")
    return moderated_text


#call the manual moderate
@app.post("/manualmoderate")
def manual_moderate_text(params: dict):
    text_input = params.get("text_input")
    #verify if the json has "text_input"
    if not text_input:
        raise HTTPException(status_code=400, detail="text_input is required")
    #clean the text
    treated_response = treat_input(text_input)
    #return the original and the moderated text
    return {"original": text_input, "moderated": treated_response}


#call the ai moderate
@app.post("/aimoderate")
def ai_moderate_text(params: dict):
    text_input = params.get("text_input")
    #verify if the json has "text_input"
    if not text_input:
        raise HTTPException(status_code=400, detail="text_input is required")
    #clean the text
    treated_response = ai_treat_input(text_input)
    #return the original and the moderated text
    return {"original": text_input, "moderated": treated_response}


# Run with: fastapi dev app.py
# Access with: http://localhost:8000/docs
