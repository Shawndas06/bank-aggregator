# Bank Aggregator API

Монолитное приложение для агрегации банковских счетов с поддержкой групп и аналитики.

## Архитектура

Проект использует **монолитную архитектуру** с FastAPI.

## Структура проекта

```
bank-aggregator/
├── main.py                 # Главный файл приложения (точка входа)
├── requirements.txt        # Зависимости Python
├── .env.example           # Пример переменных окружения
├── alembic.ini            # Конфигурация миграций
├── alembic/               # Миграции базы данных
│   └── versions/
├── src/
│   ├── config.py          # Конфигурация приложения
│   ├── database.py        # Подключение к БД
│   ├── redis_client.py    # Подключение к Redis
│   ├── dependencies.py    # Общие зависимости FastAPI
│   │
│   ├── models/            # SQLAlchemy модели (БД)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── account.py
│   │   ├── group.py
│   │   └── invitation.py
│   │
│   ├── schemas/           # Pydantic схемы (валидация)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── account.py
│   │   ├── group.py
│   │   └── common.py
│   │
│   ├── routers/           # API эндпоинты
│   │   ├── __init__.py
│   │   ├── auth.py        # BAGA
│   │   ├── accounts.py    # EZIRA
│   │   └── groups.py      # EZIRA & BAGA
│   │
│   ├── services/          # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth_service.py      # BAGA
│   │   ├── session_service.py   # BAGA
│   │   ├── otp_service.py       # BAGA
│   │   ├── account_service.py   # EZIRA
│   │   ├── bank_client.py       # EZIRA
│   │   ├── group_service.py     # EZIRA
│   │   └── invitation_service.py # BAGA
│   │
│   ├── utils/             # Вспомогательные функции
│   │   ├── __init__.py
│   │   ├── responses.py   # Стандартизированные ответы
│   │   ├── security.py    # Хеширование паролей
│   │   └── validators.py  # Дополнительные валидаторы
│   │
│   └── constants/         # Константы
│       ├── __init__.py
│       └── constants.py
```

## Установка и запуск

### 1. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Настройте переменные окружения

```bash
cp .env.example .env
# Отредактируйте .env и укажите свои настройки
```

### 4. Запустите PostgreSQL и Redis

```bash
# Через Docker
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bank_aggregator postgres:15
docker run -d --name redis -p 6379:6379 redis:7
```

### 5. Примените миграции

```bash
alembic upgrade head
```

### 6. Запустите приложение

```bash
python main.py
```

API будет доступен на `http://localhost:8000`

Документация Swagger: `http://localhost:8000/docs`

## Формат ответов API

### Успешный ответ (200)
```json
{
  "success": true,
  "data": { }
}
```

### Ошибка клиента (400)
```json
{
  "success": false,
  "error": {
    "message": "Описание ошибки"
  }
}
```

### Ошибка сервера (500)
```json
{
  "success": false,
  "error": {
    "message": "Что-то пошло не так"
  }
}
```

## Модель подписки

- **Free**: 1 группа, максимум 2 члена
- **Premium**: 5 групп, максимум 20 членов

## Поддерживаемые банки

1. VBank (id: 1)
2. SBank (id: 2)
3. ABank (id: 3)

## Разработчики

- **Baga**: Модуль аутентификации (15 часов) ⚡
- **Ezira**: Модуль счетов и групп (15 часов) ⚡

**⚠️ ВАЖНО:** Проект рассчитан на 30 часов разработки. См. `URGENT_30H_PLAN.md` для детального плана!


