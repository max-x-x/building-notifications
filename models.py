from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RegistrationLog(Base):
    __tablename__ = "registration_logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    role = Column(String(64), nullable=False)
    status = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    #ссылка на хранилище
