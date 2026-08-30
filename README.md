# Redis Simple Authorization

Минималистичный асинхронный сервис авторизации на базе **FastAPI**, **SQLAlchemy** (PostgreSQL) и **Redis**, полностью контейнеризированный через **Docker**.


## 🛠 Стек
* **Framework:** FastAPI
* **ORM:** SQLAlchemy (PostgreSQL драйвер: `asyncpg`)
* **Caching/NoSQL:** Redis
* **DevOps:** Docker / Docker Compose

## 📦 Быстрый запуск

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com
   cd Redis-simple-authorization
   ```

2. **Настройка окружения (`.env`):**
   Создайте файл `.env` в корне проекта:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=secret
   POSTGRES_DB=auth_db
   DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/auth_db

   REDIS_HOST=redis
   REDIS_PORT=6379
   TOKEN_TTL=3600
   ```

3. **Запуск через Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   *Интерфейс Swagger будет доступен по адресу:* `http://localhost:8000/docs`

## 💡 Логика работы
* **Регистрация/Вход:** Данные проверяются через **SQLAlchemy** в PostgreSQL. При успешном входе генерируется токен.
* **Сессия:** Токен записывается в **Redis** (`token: user_id`) с ограничением по времени (TTL).
* **Авторизация:** Middleware/Dependency проверяет токен напрямую в **Redis** без обращения к PostgreSQL.
