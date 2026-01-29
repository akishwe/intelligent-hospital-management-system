from fastapi import FastAPI, Depends
from app.core.config import settings
from app.modules.patient.routes import router as patient_router
from app.modules.auth.router import router as auth_router
from app.core.deps import get_current_user

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(patient_router, dependencies=[Depends(get_current_user)])
app.include_router(auth_router)


@app.get("/")
def health_check():
    return {"status": "running", "app_name": settings.app_name}

