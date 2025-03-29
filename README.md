# Yatube API

Yatube API — это API для социальной сети с возможностью публиковать посты, комментировать их, вступать в сообщества и подписываться на других пользователей.

Документация доступна по адресу: http://127.0.0.1:8000/redoc/

## Возможности

- Аутентификация через JWT
- Создание и редактирование постов
- Комментирование постов
- Просмотр сообществ
- Подписка на пользователей

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/your-username/api_final_yatube.git
cd api_final_yatube/yatube_api
```

2. Создать и активировать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Применить миграции и создать суперпользователя:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Запустить сервер:
```bash
python manage.py runserver
```

## Примеры запросов

POST /api/v1/jwt/create/ — получить токен  
POST /api/v1/posts/ — создать пост  
GET /api/v1/posts/{id}/comments/ — список комментариев  
POST /api/v1/follow/ — подписаться на пользователя

## Тестирование

```bash
pytest
```
