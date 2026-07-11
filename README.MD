# Coursework 5 — Habit Tracker

Сервис для отслеживания полезных привычек с напоминаниями через Telegram.

## Стек

- Python 3.14
- Django 6.0
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Telegram Bot API
- drf-spectacular

## Установка

1. Клонировать репозиторий и перейти в папку
2. Установить зависимости: poetry install
3. Создать .env файл по шаблону .env.template и заполнить переменные
4. Применить миграции: python manage.py migrate
5. Запустить сервер: python manage.py runserver

## Запуск Celery

celery -A config worker --loglevel=info
celery -A config beat --loglevel=info

## Переменные окружения

DATABASE_NAME — имя базы данных
DATABASE_USER — пользователь БД
DATABASE_PASSWORD — пароль БД
DATABASE_HOST — хост БД
DATABASE_PORT — порт БД
REDIS_URL — URL Redis брокера
TELEGRAM_BOT_TOKEN — токен Telegram бота

## API Документация

Swagger UI: http://localhost:8000/api/docs/
ReDoc: http://localhost:8000/api/redoc/

## Эндпоинты

POST   /users/register/        — Регистрация
POST   /users/login/           — Получение JWT токена
POST   /users/token/refresh/   — Обновление токена
GET    /users/profile/         — Профиль пользователя
PATCH  /users/profile/         — Обновление профиля
GET    /habits/                — Список привычек
POST   /habits/                — Создание привычки
GET    /habits/<id>/           — Получение привычки
PUT    /habits/<id>/           — Обновление привычки
DELETE /habits/<id>/           — Удаление привычки
GET    /habits/public/         — Публичные привычки

## Тесты

python manage.py test
coverage run manage.py test && coverage report