# Bank Aggregator API

Монолитное приложение для агрегации банковских счетов с поддержкой групп.

**Хакатон:** VTB API 2025  
**Команда:** team222  
**Архитектура:** Монолит

---

## Быстрый старт

```bash
docker-compose up -d
```

**API:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs

---

## Credentials

```
Team ID:     team222
Team Secret: Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT
```

---

## Структура проекта

```
bank-aggregator/
├── main.py              # Точка входа
├── init_db.py           # Инициализация БД
├── docker-compose.yaml  # Оркестрация
├── Dockerfile
├── requirements.txt
└── src/
    ├── routers/         # 3 роутера (26 эндпоинтов)
    ├── services/        # 7 сервисов
    ├── models/          # 6 моделей БД
    ├── schemas/         # Pydantic схемы
    ├── utils/           # Утилиты
    └── constants/       # Константы
```

---

## API Эндпоинты

### Auth (5)
```
POST   /api/auth/sign-up
POST   /api/auth/verify-email
POST   /api/auth/sign-in
GET    /api/auth/me
POST   /api/auth/logout
```

### Accounts (7)
```
GET    /api/accounts
POST   /api/accounts
POST   /api/accounts/attach
GET    /api/accounts/{id}?client_id=1
GET    /api/accounts/{id}/balances?client_id=1
GET    /api/accounts/{id}/transactions?client_id=1
```

### Groups (14)
```
POST   /api/groups
GET    /api/groups
GET    /api/groups/settings
GET    /api/groups/invites
POST   /api/groups/invite
POST   /api/groups/invite/accept
POST   /api/groups/invite/decline
GET    /api/groups/{id}/accounts
GET    /api/groups/{id}/accounts/balances
GET    /api/groups/{id}/accounts/transactions
DELETE /api/groups
POST   /api/groups/exit
```

---

## Интеграция с банками

| Банк | ID | URL | Статус |
|------|-----|-----|---------|
| VBank | 1 | vbank.open.bankingapi.ru | ✅ Авто-одобрение |
| SBank | 2 | sbank.open.bankingapi.ru | ⚠️ Ручное одобрение |
| ABank | 3 | abank.open.bankingapi.ru | ✅ Авто-одобрение |

---

## Формат данных

### Request Body - camelCase
```json
{
  "email": "user@example.com",
  "password": "Test123456",
  "name": "User",
  "birthDate": "2000-01-01",
  "clientId": 1,
  "groupId": 1
}
```

### Response - camelCase
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "User",
    "birthDate": "2000-01-01",
    "accountType": "free"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "message": "Описание ошибки"
  }
}
```

---

## Технологии

- **FastAPI** - Web framework
- **PostgreSQL** - База данных
- **Redis** - Кеширование и сессии
- **SQLAlchemy** - ORM
- **Pydantic** - Валидация
- **httpx** - HTTP клиент
- **bcrypt** - Хеширование паролей

---

## Docker Compose

### Запуск
```bash
docker-compose up -d
```

### Логи
```bash
docker-compose logs -f backend
```

### Остановка
```bash
docker-compose down
```

### Пересборка
```bash
docker-compose up -d --build
```

---

## Health Check

```bash
curl http://localhost:8000/health
```

**Ответ:**
```json
{
  "success": true,
  "data": {
    "api": "healthy",
    "redis": "healthy",
    "version": "1.0.0"
  }
}
```

---

## Примеры запросов

### Регистрация
```bash
curl -X POST http://localhost:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "name": "Test User",
    "birthDate": "2000-01-01"
  }'
```

### Подтверждение email
```bash
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "otpCode": "123456"
  }' \
  -c cookies.txt
```

### Создание счёта
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"clientId": 1}' \
  -b cookies.txt
```

---

## CORS

Настроен для:
- http://localhost:3000
- http://localhost:5173
- http://localhost:8080

---

## Кеширование в Redis

| Что | TTL |
|-----|-----|
| Токен банка | 23ч |
| Consent | 4ч |
| Баланс | 4ч |
| Транзакции | 4ч |
| Сессия | 24ч |

---

## Лимиты групп

```json
{
  "free": {
    "maxGroups": 1,
    "maxMembers": 2
  },
  "premium": {
    "maxGroups": 5,
    "maxMembers": 20
  }
}
```

---

## Production Ready

✅ Код без комментариев  
✅ Монолитная архитектура  
✅ Интеграция с реальными банками  
✅ Кеширование данных  
✅ CORS настроен  
✅ Валидация данных  
✅ Безопасность (bcrypt, HTTP-only cookies)

---

**Swagger UI:** http://localhost:8000/docs
