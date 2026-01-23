from fastapi import FastAPI
from app.core.config import settings
from app.modules.patient.routes import router as patient_router
from app.modules.patient import models

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(patient_router)


@app.get("/")
def health_check():
    return {"status": "running", "app_name": settings.app_name}

