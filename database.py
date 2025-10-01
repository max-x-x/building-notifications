from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import time

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "myapp")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def wait_for_db():
    """Ожидает готовности базы данных"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                return engine
        except Exception as e:
            retry_count += 1
            print(f"Ожидание БД... попытка {retry_count}/{max_retries}")
            time.sleep(2)
    
    raise Exception("Не удалось подключиться к базе данных")

engine = wait_for_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создает все таблицы в БД"""
    Base.metadata.create_all(bind=engine)