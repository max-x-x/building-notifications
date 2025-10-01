# Notification Service

FastAPI сервис для отправки уведомлений с PostgreSQL базой данных.

## Запуск через Docker

1. Создайте файл `.env` в корне проекта:
```
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=postgres
DB_PORT=5432
DB_NAME=myapp
login=your_email@yandex.ru
password=your_password
```

2. Запустите сервисы:
```bash
docker-compose up --build
```

3. API будет доступен на `http://localhost:8000`
4. Документация API: `http://localhost:8000/docs`

## API Endpoints

- `POST /send-notification` - отправка уведомления пользователю
- `POST /send-role-notification` - отправка HTML уведомления для роли
