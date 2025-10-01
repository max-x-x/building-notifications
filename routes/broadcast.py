from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import send_notification
import requests
import os

router = APIRouter(prefix="/broadcast", tags=["broadcast"])

class BroadcastRequest(BaseModel):
    to: str  # ssk, iko, foreman
    subject: str
    body: str
    is_html: bool = False
    access_token: str

@router.post("/notification")
async def broadcast_notification(request: BroadcastRequest):
    try:
        print(f"🔧 [BROADCAST] Начало обработки запроса для роли: {request.to}")
        
        # Используем токен из запроса
        access_token = request.access_token
        print(f"🔧 [BROADCAST] Токен получен: {access_token[:10]}...")
        
        # Получаем список пользователей по роли
        role_mapping = {
            "ssk": "ssk",
            "iko": "iko", 
            "foreman": "foreman",
            "all": None  # для всех ролей
        }
        
        role = role_mapping.get(request.to)
        if role is None and request.to != "all":
            print(f"❌ [BROADCAST] Неверная роль: {request.to}")
            raise HTTPException(status_code=400, detail="Неверная роль. Доступные: ssk, iko, foreman, all")
        
        print(f"🔧 [BROADCAST] Роль определена: {role}")
        
        # Для роли "all" не передаем параметр role
        params = {"role": role} if role else {}
        print(f"🔧 [BROADCAST] Отправляем запрос к API с параметрами: {params}")
        
        resp = requests.get(
            'https://building-api.itc-hub.ru/api/v1/users',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            params=params,
            timeout=15
        )
        
        print(f"🔧 [BROADCAST] Ответ API: статус {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"❌ [BROADCAST] Ошибка API: {resp.status_code}, текст: {resp.text}")
            raise HTTPException(status_code=502, detail=f"Ошибка API: {resp.status_code}")
        
        data = resp.json()
        users = data.get("items", [])
        print(f"🔧 [BROADCAST] Получено пользователей: {len(users)}")
        
        if not users:
            print("ℹ️ [BROADCAST] Пользователи с такой ролью не найдены")
            return {"status": "success", "message": "Пользователи с такой ролью не найдены", "sent_count": 0}
        
        # Отправляем уведомления всем пользователям
        sent_count = 0
        print(f"🔧 [BROADCAST] Начинаем отправку уведомлений...")
        
        for i, user in enumerate(users):
            email = user.get("email")
            user_id = user.get("id")
            print(f"🔧 [BROADCAST] Пользователь {i+1}: email={email}, id={user_id}")
            
            if email and user_id:
                print(f"🔧 [BROADCAST] Отправляем уведомление на {email}")
                success = send_notification([email], request.subject, request.body, str(user_id), request.is_html)
                if success:
                    sent_count += 1
                    print(f"✅ [BROADCAST] Уведомление отправлено на {email}")
                else:
                    print(f"❌ [BROADCAST] Ошибка отправки на {email}")
            else:
                print(f"⚠️ [BROADCAST] Пропускаем пользователя {i+1}: нет email или id")
        
        print(f"🔧 [BROADCAST] Завершено. Отправлено: {sent_count}/{len(users)}")
        
        return {
            "status": "success", 
            "message": f"Отправлено {sent_count} из {len(users)} уведомлений",
            "sent_count": sent_count,
            "total_users": len(users)
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ошибка подключения к API: {str(e)}")
    except Exception as e:
        import traceback
        error_msg = f"Ошибка: {str(e)}. Traceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_msg)
