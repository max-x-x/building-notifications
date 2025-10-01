from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import send_notification

router = APIRouter(prefix="/send", tags=["send"])

class NotificationRequest(BaseModel):
    user_id: str
    email: str
    subject: str
    message: str

@router.post("/notification")
async def send_user_notification(request: NotificationRequest):
    try:
        result = send_notification([request.email], request.subject, request.message, request.user_id)
        if result:
            return {"status": "success", "message": "Уведомление отправлено"}
        else:
            raise HTTPException(status_code=502, detail="Ошибка отправки email (SMTP)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
