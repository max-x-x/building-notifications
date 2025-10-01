from EmailClent import EmailClient
import os
from dotenv import load_dotenv
from database import SessionLocal
from models import Notification

load_dotenv()

def send_notification(to, subject, body, user_id=None, is_html=False):
    db = None
    try:
        yandex_client = EmailClient(
            smtp_server="smtp.yandex.ru",
            port=587,
            email=os.getenv("login"),
            password=os.getenv("password")
        )

        send_success = yandex_client.send_email(to_emails=to, subject=subject, body=body, is_html=is_html)

        db = SessionLocal()

        for recipient in to:
            new_notification = Notification(
                user_id=user_id,
                recipient=recipient,
                subject=subject,
                body=body,
                status="sent" if send_success else "failed",
                is_read=False
            )
            db.add(new_notification)

        db.commit()

        return send_success

    except Exception as e:
        if db:
            db.rollback()
        return False

    finally:
        if db:
            db.close()