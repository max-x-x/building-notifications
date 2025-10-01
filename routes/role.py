from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import send_notification
import os

router = APIRouter(prefix="/role", tags=["role"])

class RoleNotificationRequest(BaseModel):
    role_id: str
    email: str

@router.post("/notification")
async def send_role_notification(request: RoleNotificationRequest):
    try:
        link = f"{os.getenv('PUBLIC_BASE_URL', 'http://localhost:8000')}/templates/{request.role_id}?email={request.email}"
        subject = f"Приглашение к регистрации — {request.role_id.upper()}"

        styles = """
        <style>
        .card{max-width:560px;margin:24px auto;font-family:Arial,Helvetica,sans-serif;border:1px solid #e6e6e6;border-radius:10px;overflow:hidden}
        .header{background:#111827;color:#fff;padding:16px 20px;font-size:18px;font-weight:700}
        .body{padding:20px;color:#111827;line-height:1.5}
        .btn{display:inline-block;background:#3b82f6;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600}
        .note{color:#6b7280;font-size:12px;margin-top:12px}
        </style>
        """

        role_titles = {"ssk":"ССК","iko":"ИКО","prorab":"Прораб"}
        title = role_titles.get(request.role_id, request.role_id)

        body = f"""
        {styles}
        <div class=card>
          <div class=header>Приглашение к регистрации</div>
          <div class=body>
            <p>Вам доступна регистрация для роли <b>{title}</b>.</p>
            <p>Перейдите по ссылке ниже, чтобы заполнить короткую форму:</p>
            <p><a class=btn href="{link}" target="_blank">Перейти к регистрации</a></p>
            <p class=note>Если кнопка не работает, скопируйте ссылку в браузер:<br>{link}</p>
          </div>
        </div>
        """

        ok = send_notification([request.email], subject, body, 0, is_html=True)
        if not ok:
            raise HTTPException(status_code=502, detail="Ошибка отправки email (SMTP)")
        return {"status": "success", "message": "Ссылка на регистрацию отправлена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
