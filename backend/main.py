from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router as api_router
from backend.db import engine, Base

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Mount static files for dashboard (serves CSS, JS, images)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include API and dashboard routes
app.include_router(api_router) 