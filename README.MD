# Coursework 5 — Habit Tracker

Сервис для отслеживания полезных привычек с напоминаниями через Telegram.

## Стек

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- Redis
- Celery + Celery Beat
- Telegram Bot API
- Nginx
- Docker + Docker Compose
- GitHub Actions

## Запуск локально

1. Клонировать репозиторий:
   git clone https://github.com/KirlRj/coursework_5.git
   cd coursework_5

2. Создать .env файл по шаблону .env.template и заполнить переменные

3. Запустить проект:
   docker compose up --build

4. Применить миграции (в отдельном терминале):
   docker compose exec web python manage.py migrate

5. Приложение доступно на http://localhost/

## Переменные окружения

DATABASE_NAME — имя базы данных
DATABASE_USER — пользователь БД
DATABASE_PASSWORD — пароль БД
DATABASE_HOST — хост БД
DATABASE_PORT — порт БД
REDIS_URL — URL Redis брокера
TELEGRAM_BOT_TOKEN — токен Telegram бота

## API Документация

Swagger UI: http://localhost/api/docs/
ReDoc: http://localhost/api/redoc/

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

## Тесты и линтинг

python manage.py test
flake8 habits users config --max-line-length=119

## CI/CD

При каждом push в ветки main или feature_2 GitHub Actions автоматически:
1. Запускает тесты и линтинг
2. Проверяет сборку Docker образов
3. Деплоит проект на сервер

### Настройка деплоя

Добавь секреты в GitHub Settings -> Secrets -> Actions:
- SERVER_HOST — IP адрес сервера
- SERVER_USER — пользователь сервера
- SERVER_KEY — приватный SSH ключ

## Остановка проекта

docker compose down

Для удаления данных:
docker compose down -v