from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from backend.db import SessionLocal
from backend.services.moderation import treat_input, ai_treat_input
from backend.services.filters import get_prohibited_words, add_filter_word, delete_filter_word
from backend.services.logs import add_log, get_recent_logs, get_all_logs

router = APIRouter()
# Set the directory for Jinja2 templates (HTML pages)
templates = Jinja2Templates(directory="frontend/templates")

# Pydantic model for API input
class TextInput(BaseModel):
    text_input: str

# Manual moderation API endpoint
@router.post("/manualmoderate")
def manual_moderate_text(params: TextInput):
    """
    Receives text input and applies manual moderation using the word filter.
    Logs the moderation event in the database.
    """
    db = SessionLocal()
    text_input = params.text_input
    if not text_input:
        db.close()
        raise HTTPException(status_code=400, detail="text_input is required")
    prohibited_words = get_prohibited_words(db)
    treated_response = treat_input(text_input, prohibited_words)
    add_log(db, text_input, treated_response, "manual")
    db.close()
    return {"original": text_input, "moderated": treated_response}

# AI moderation API endpoint
@router.post("/aimoderate")
def ai_moderate_text(params: TextInput):
    """
    Receives text input and applies AI-based moderation.
    Logs the moderation event in the database.
    """
    db = SessionLocal()
    text_input = params.text_input
    if not text_input:
        db.close()
        raise HTTPException(status_code=400, detail="text_input is required")
    treated_response = ai_treat_input(text_input)
    add_log(db, text_input, treated_response, "ai")
    db.close()
    return {"original": text_input, "moderated": treated_response}

# Dashboard home page
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """
    Renders the dashboard home page with the most recent moderation logs.
    """
    db = SessionLocal()
    logs = get_recent_logs(db, limit=10)
    db.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs})

# Filters management page
@router.get("/filters", response_class=HTMLResponse)
def filters_page(request: Request):
    """
    Renders the filters management page, listing all prohibited words.
    """
    db = SessionLocal()
    filters = db.query(getattr(db.registry.mapped, 'FilterWord', None) or db.registry._class_registry['FilterWord']).all()
    db.close()
    return templates.TemplateResponse("filters.html", {"request": request, "filters": filters})

@router.post("/filters/add")
def add_filter(request: Request, word: str = Form(...)):
    """
    Adds a new word to the filter list.
    """
    db = SessionLocal()
    add_filter_word(db, word)
    db.close()
    return RedirectResponse("/filters", status_code=303)

@router.post("/filters/delete/{filter_id}")
def delete_filter(request: Request, filter_id: int):
    """
    Deletes a word from the filter list by its ID.
    """
    db = SessionLocal()
    delete_filter_word(db, filter_id)
    db.close()
    return RedirectResponse("/filters", status_code=303)

# Logs page
@router.get("/logs", response_class=HTMLResponse)
def logs_page(request: Request):
    """
    Renders the logs page, showing all moderation events.
    """
    db = SessionLocal()
    logs = get_all_logs(db)
    db.close()
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

# Settings page (placeholder)
@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    """
    Renders the settings page (currently a placeholder).
    """
    return templates.TemplateResponse("settings.html", {"request": request}) 