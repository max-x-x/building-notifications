from fastapi import FastAPI
from routes import notifications, send, role, templates, ping, register_log, broadcast
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables

app = FastAPI()

# Создаем таблицы при запуске
create_tables()

# CORS: разрешить любой Origin, все методы и заголовки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # любой источник
    allow_methods=["*"],      # любые HTTP-методы
    allow_headers=["*"],      # любые заголовки
    # allow_credentials=False  # по умолчанию False; с "*" нельзя True
)

app.include_router(notifications.router)
app.include_router(send.router)
app.include_router(role.router)
app.include_router(templates.router)
app.include_router(ping.router)
app.include_router(register_log.router)
app.include_router(broadcast.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
