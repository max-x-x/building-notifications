from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Notification

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/{user_id}")
async def get_user_notifications(user_id: str):
    try:
        db = SessionLocal()
        notifications = db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()
        db.close()
        
        return {
            "user_id": user_id,
            "notifications": [
                {
                    "id": n.id,
                    "subject": n.subject,
                    "body": n.body,
                    "status": n.status,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat()
                }
                for n in notifications
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    try:
        db = SessionLocal()
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if not notification:
            db.close()
            raise HTTPException(status_code=404, detail="Уведомление не найдено")
        
        notification.is_read = True
        db.commit()
        db.close()
        
        return {"status": "success", "message": "Уведомление отмечено как прочитанное"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
