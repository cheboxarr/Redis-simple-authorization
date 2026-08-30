# Redis Simple Authorization

Минималистичный асинхронный сервис авторизации на базе **FastAPI**, **SQLAlchemy** (MySQL) и **Redis**, полностью контейнеризированный через **Docker**.


## 🛠 Стек
* **Framework:** FastAPI
* **ORM:** SQLAlchemy (MySQL)
* **Caching/NoSQL:** Redis
* **DevOps:** Docker / Docker Compose

## 📦 Быстрый запуск

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com
   cd Redis-simple-authorization
   ```

2. **Настройка окружения (`.env`):**
   Создайте файл `.env` в корне проекта, и скопируйте из .env.example данные(добавив свой пароль)


3. **Запуск через Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   *Интерфейс Swagger будет доступен по адресу:* `http://localhost:8000/docs`

## 💡 Логика работы
* **Регистрация/Вход:** Данные проверяются через **SQLAlchemy** в MySQL. При успешном входе генерируется токен.
* **Сессия:** Токен записывается в **Redis** (`token: user_id`) с ограничением по времени (TTL).
* **Авторизация:** Middleware/Dependency проверяет токен напрямую в **Redis** без обращения к MySQL.
