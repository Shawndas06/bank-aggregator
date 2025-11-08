# 🏦 Bank Aggregator API

**Монолитное приложение для агрегации банковских счетов с поддержкой групп**

Проект для хакатона VTB API 2025 - Кейс "Мультибанк"

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Запуск PostgreSQL и Redis

```bash
# Через Docker
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=bank_aggregator postgres:15

docker run -d --name redis -p 6379:6379 redis:7
```

### 3. Инициализация БД

```bash
python init_db.py
```

### 4. Запуск

```bash
python main.py
```

**API:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs

---

## 🔑 Credentials (VTB Hackathon 2025)

```
Team ID:     team222
Team Secret: Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT
Sandbox:     https://open.bankingapi.ru/ (пароль: 321)
```

Credentials уже настроены в `src/config.py`!

---

## 📋 API Эндпоинты

### 🔐 Аутентификация

```
POST   /api/auth/sign-up          Регистрация
POST   /api/auth/verify-email     Подтверждение email (OTP: 123456)
POST   /api/auth/sign-in          Вход
GET    /api/auth/me               Текущий пользователь
POST   /api/auth/logout           Выход
```

### 💳 Счета

```
GET    /api/accounts                      Список счетов
POST   /api/accounts                      Создать счёт
POST   /api/accounts/attach               Привязать счёт
GET    /api/accounts/{id}                 Информация о счёте
GET    /api/accounts/{id}/balances        Баланс
GET    /api/accounts/{id}/transactions    Транзакции
```

### 👥 Группы

```
POST   /api/groups                        Создать группу
GET    /api/groups                        Список групп
GET    /api/groups/settings               Лимиты (free/premium)
DELETE /api/groups                        Удалить группу
POST   /api/groups/exit                   Выйти из группы
GET    /api/groups/{id}/accounts          Счета группы
GET    /api/groups/{id}/accounts/balances Балансы группы
POST   /api/groups/invite                 Пригласить в группу
POST   /api/groups/invite/accept          Принять приглашение
POST   /api/groups/invite/decline         Отклонить приглашение
```

---

## 📊 Формат ответов

### Успех (200, 201)
```json
{
  "success": true,
  "data": {...}
}
```

### Ошибка (400, 401, 403, 404)
```json
{
  "success": false,
  "error": {
    "message": "Описание ошибки"
  }
}
```

**Naming:** API использует `camelCase` (birthDate, accountType, isActive)

---

## 🏗️ Архитектура

**Монолитная архитектура на FastAPI**

```
bank-aggregator/
├── main.py                  # Точка входа
├── init_db.py              # Инициализация БД
├── test_api.py             # Тестирование
├── requirements.txt
├── src/
│   ├── config.py           # Конфигурация (credentials здесь!)
│   ├── database.py         # PostgreSQL
│   ├── redis_client.py     # Redis
│   ├── dependencies.py     # FastAPI dependencies
│   ├── models/             # SQLAlchemy модели
│   │   ├── user.py
│   │   ├── otp_code.py
│   │   ├── account.py
│   │   ├── group.py
│   │   └── invitation.py
│   ├── schemas/            # Pydantic схемы
│   │   ├── auth.py
│   │   ├── account.py
│   │   └── group.py
│   ├── routers/            # API эндпоинты
│   │   ├── auth.py
│   │   ├── accounts.py
│   │   └── groups.py
│   ├── services/           # Бизнес-логика
│   │   ├── auth_service.py
│   │   ├── session_service.py
│   │   ├── otp_service.py
│   │   ├── bank_client.py         # Интеграция с банками
│   │   ├── account_service.py
│   │   ├── group_service.py
│   │   └── invitation_service.py
│   ├── utils/              # Утилиты
│   │   ├── responses.py
│   │   ├── security.py
│   │   └── validators.py
│   └── constants/          # Константы
│       ├── constants.py
│       └── bank_config.py
```

---

## 🏦 Интеграция с банками

Backend интегрирован с **реальным OpenBanking API** трёх банков:

| Банк | URL | ID |
|------|-----|-----|
| VBank | https://vbank.open.bankingapi.ru | 1 |
| ABank | https://abank.open.bankingapi.ru | 3 |
| SBank | https://sbank.open.bankingapi.ru | 2 |

### Как это работает:

```
1. Получение токена банка (кеш: 23 часа)
   POST /auth/bank-token?client_id=team222&client_secret=xxx
   
2. Создание consent - согласия на доступ (кеш: 4 часа)
   POST /account-consents/request
   Headers: X-Requesting-Bank: team222
   
3. Получение данных (кеш: 4 часа)
   GET /accounts?client_id=team222-{user_id}
   Headers: Authorization, X-Requesting-Bank, X-Consent-Id
```

**Все данные кешируются в Redis для производительности!**

---

## 🔐 Безопасность

- ✅ Пароли хешируются (bcrypt)
- ✅ HTTP-only cookie для сессий
- ✅ JWT токены от банков (RS256)
- ✅ Consents для межбанкового доступа
- ✅ Валидация всех входных данных (Pydantic)

---

## 📦 Модель данных

**6 моделей БД:**
- `User` - пользователи
- `OTPCode` - коды подтверждения email
- `BankAccount` - банковские счета
- `Group` - группы
- `GroupMember` - членство в группах
- `Invitation` - приглашения в группы

**Лимиты аккаунтов:**
- **Free**: 1 группа, 2 члена
- **Premium**: 5 групп, 20 членов

---

## 🧪 Тестирование

### Автоматическое тестирование

```bash
python test_api.py
```

Протестирует:
- Регистрация → Подтверждение → Вход
- Создание счёта → Баланс → Транзакции
- Создание группы → Счета группы

### Через Swagger UI

```
http://localhost:8000/docs
```

1. POST /api/auth/sign-up - зарегистрироваться
2. POST /api/auth/verify-email - подтвердить (код: 123456)
3. POST /api/accounts - создать счёт (реальные данные из VBank!)

### Через curl

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123456","name":"Test","birthDate":"2000-01-01"}'

# Подтверждение
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","code":"123456"}' \
  -c cookies.txt

# Создание счёта (РЕАЛЬНЫЕ ДАННЫЕ!)
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"client_id":1}' \
  -b cookies.txt
```

---

## 📚 Полная документация API

См. **`API_DOCUMENTATION.md`** для детальной документации всех эндпоинтов с примерами.

---

## 🎯 Для Frontend разработчика

### Cookie-based аутентификация

После `/sign-in` или `/verify-email` сервер устанавливает `session-id` cookie (httpOnly).

**JavaScript/Fetch:**
```javascript
fetch('http://localhost:8000/api/auth/me', {
  credentials: 'include'  // ВАЖНО!
})
```

**Axios:**
```javascript
axios.defaults.withCredentials = true;
```

### Naming Convention

- **БД**: `snake_case` (user_id, created_at)
- **API**: `camelCase` (userId, createdAt)

### CORS

Разрешены origins:
```
http://localhost:3000
http://localhost:5173
http://localhost:8080
```

---

## 🚨 Troubleshooting

### Backend использует mock данные?

**Проверьте credentials:**
```bash
# Должно быть:
TEAM_CLIENT_ID=team222
TEAM_CLIENT_SECRET=Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT
```

### Ошибка подключения к БД?

```bash
docker ps | grep postgres
# Если нет - запустите:
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=bank_aggregator postgres:15
```

### Ошибка подключения к Redis?

```bash
docker ps | grep redis
# Если нет - запустите:
docker run -d --name redis -p 6379:6379 redis:7
```

---

## 📊 Кеширование в Redis

| Что | Ключ | TTL |
|-----|------|-----|
| Токен банка | `bank_token:{user_id}:{bank_id}` | 23ч |
| Consent | `consent:{user_id}:{bank_id}` | 4ч |
| Баланс | `balance:{user_id}:{account_id}` | 4ч |
| Транзакции | `transactions:{user_id}:{account_id}` | 4ч |
| Сессия | `session:{session_id}` | 24ч |
| OTP | `otp:{email}` | 10мин |

---

## 🛠️ Технологии

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - База данных
- **Redis** - Кеширование и сессии
- **Pydantic** - Валидация
- **httpx** - HTTP клиент для банков
- **bcrypt** - Хеширование паролей

---

## 👥 Команда

- **Baga** - Аутентификация, сессии, OTP, приглашения
- **Ezira** - Счета, банковская интеграция, группы

**Хакатон:** VTB API 2025 - Кейс "Мультибанк"  
**Команда:** team222

---

## ✅ Статус проекта

✅ **25 эндпоинтов** реализованы  
✅ **Интеграция с реальными банками** (VBank, ABank, SBank)  
✅ **Кеширование** для производительности  
✅ **Полная документация** для Frontend  
✅ **Готов к production** 🚀

---

**Backend готов! Frontend может начинать интеграцию!** 🎉
