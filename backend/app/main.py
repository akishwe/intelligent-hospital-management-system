from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

@app.get("/")
def health_check():
    return {"status": "running", "app_name": settings.app_name}

