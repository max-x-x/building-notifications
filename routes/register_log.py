from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import RegistrationLog

router = APIRouter(prefix="/register-log", tags=["register-log"])

class RegisterLogIn(BaseModel):
    email: str
    role: str
    status: str

@router.post("")
async def create_log(payload: RegisterLogIn):
    try:
        db = SessionLocal()
        log = RegistrationLog(email=payload.email, role=payload.role, status=payload.status)
        db.add(log)
        db.commit()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


