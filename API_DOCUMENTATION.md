# 📚 API Documentation для Frontend

## Base URL
```
http://localhost:8000
```

## 🔐 Credentials (VTB Hackathon 2025)

```
Team ID:     team222
Team Secret: Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT
```

Backend уже настроен с этими credentials!

---

## 📋 Формат ответов

### ✅ Успех
```json
{
  "success": true,
  "data": {...}
}
```

### ❌ Ошибка
```json
{
  "success": false,
  "error": {
    "message": "Описание ошибки"
  }
}
```

---

## 🔐 Аутентификация

### 1. Регистрация
```http
POST /api/auth/sign-up
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123",
  "name": "Иван Иванов",
  "birthDate": "2000-01-01"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "message": "Регистрация успешна! Проверьте email для подтверждения.",
    "email": "user@example.com",
    "otpCode": "123456"
  }
}
```

---

### 2. Подтверждение Email (OTP)
```http
POST /api/auth/verify-email
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response (200) + Cookie `session-id`:**
```json
{
  "success": true,
  "data": {
    "message": "Email подтверждён!",
    "user": {
      "id": 1,
      "name": "Иван Иванов",
      "birthDate": "2000-01-01",
      "accountType": "free"
    }
  }
}
```

---

### 3. Вход
```http
POST /api/auth/sign-in
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123"
}
```

**Response (200) + Cookie `session-id`:**
```json
{
  "success": true,
  "data": {
    "message": "Вход выполнен успешно",
    "user": {
      "id": 1,
      "name": "Иван Иванов",
      "birthDate": "2000-01-01",
      "accountType": "free"
    }
  }
}
```

---

### 4. Текущий пользователь
```http
GET /api/auth/me
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Иван Иванов",
    "birthDate": "2000-01-01",
    "accountType": "free"
  }
}
```

---

### 5. Выход
```http
POST /api/auth/logout
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Выход выполнен успешно"
  }
}
```

---

## 💳 Счета

### 1. Список счетов
```http
GET /api/accounts
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "accountId": "acc-3311",
      "accountName": "Checking счет",
      "clientId": 1,
      "clientName": "vbank",
      "isActive": true
    }
  ]
}
```

**С фильтром по банку:**
```http
GET /api/accounts?client_id=1
```

---

### 2. Создать счёт
```http
POST /api/accounts
Cookie: session-id=...
Content-Type: application/json

{
  "client_id": 1
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "message": "Счёт успешно создан",
    "account": {
      "accountId": "acc-3311",
      "accountName": "Checking счет",
      "clientId": 1,
      "isActive": true
    }
  }
}
```

**Доступные банки:**
- `1` - VBank
- `2` - SBank  
- `3` - ABank

---

### 3. Привязать счёт
```http
POST /api/accounts/attach
Cookie: session-id=...
Content-Type: application/json

{
  "id": 1
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Счёт успешно привязан",
    "accountId": 1
  }
}
```

---

### 4. Информация о счёте
```http
GET /api/accounts/{account_id}?client_id=1
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "accountId": "acc-3311",
    "accountName": "Checking счет",
    "clientId": 1,
    "clientName": "vbank",
    "isActive": true
  }
}
```

---

### 5. Баланс счёта
```http
GET /api/accounts/{account_id}/balances?client_id=1
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "amount": 15432.50,
    "currency": "RUB"
  }
}
```

**⚡ Кешируется на 4 часа!**

---

### 6. Транзакции счёта
```http
GET /api/accounts/{account_id}/transactions?client_id=1
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "txn-12345",
      "date": "2025-11-08T10:30:00",
      "description": "Покупка в магазине",
      "amount": -500.00,
      "currency": "RUB",
      "type": "debit"
    }
  ]
}
```

**⚡ Кешируется на 4 часа!**

---

## 👥 Группы

### 1. Создать группу
```http
POST /api/groups
Cookie: session-id=...
Content-Type: application/json

{
  "name": "Моя семья"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Моя семья",
    "ownerId": 1,
    "createdAt": "2025-11-08T10:00:00"
  }
}
```

---

### 2. Список групп
```http
GET /api/groups
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Моя семья",
      "ownerId": 1,
      "createdAt": "2025-11-08T10:00:00"
    }
  ]
}
```

---

### 3. Настройки групп
```http
GET /api/groups/settings
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "free": {
      "maxGroups": 1,
      "maxMembers": 2
    },
    "premium": {
      "maxGroups": 5,
      "maxMembers": 20
    }
  }
}
```

---

### 4. Пригласить в группу
```http
POST /api/groups/invite
Cookie: session-id=...
Content-Type: application/json

{
  "group_id": 1,
  "email": "friend@example.com"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "message": "Приглашение успешно отправлено",
    "requestId": 1
  }
}
```

---

### 5. Принять приглашение
```http
POST /api/groups/invite/accept
Cookie: session-id=...
Content-Type: application/json

{
  "request_id": 1
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Приглашение принято успешно"
  }
}
```

---

### 6. Отклонить приглашение
```http
POST /api/groups/invite/decline
Cookie: session-id=...
Content-Type: application/json

{
  "request_id": 1
}
```

---

### 7. Счета группы
```http
GET /api/groups/{group_id}/accounts
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "owner": {
        "name": "Иван"
      },
      "clientId": "1",
      "clientName": "vbank",
      "accountId": "acc-3311",
      "accountName": "Checking счет"
    }
  ]
}
```

---

### 8. Балансы группы
```http
GET /api/groups/{group_id}/accounts/balances
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "clientId": "1",
      "name": "vbank",
      "accountName": "Checking счет",
      "owner": {
        "name": "Иван"
      },
      "balance": {
        "amount": 15000.50,
        "currency": "RUB"
      }
    }
  ]
}
```

---

### 9. Транзакции группы
```http
GET /api/groups/{group_id}/accounts/transactions
Cookie: session-id=...
```

---

### 10. Удалить группу
```http
DELETE /api/groups
Cookie: session-id=...
Content-Type: application/json

{
  "groupId": 1
}
```

---

### 11. Выйти из группы
```http
POST /api/groups/exit
Cookie: session-id=...
Content-Type: application/json

{
  "groupId": 1
}
```

---

## 🏦 Интеграция с банками

Backend интегрирован с **реальными OpenBanking API**:

| Банк | URL | Авто-одобрение |
|------|-----|----------------|
| VBank | vbank.open.bankingapi.ru | ✅ Да |
| ABank | abank.open.bankingapi.ru | ✅ Да |
| SBank | sbank.open.bankingapi.ru | ⚠️ Требует подтверждения |

### Как это работает:

1. **Получение токена** (23 часа кеш)
2. **Создание consent** (4 часа кеш)
3. **Запрос данных** (4 часа кеш)

Все операции **автоматические** - Frontend просто вызывает эндпоинты!

---

## 🍪 Работа с Cookie

### JavaScript (Fetch)
```javascript
fetch('http://localhost:8000/api/auth/me', {
  credentials: 'include'
})
```

### JavaScript (Axios)
```javascript
axios.defaults.withCredentials = true;
```

---

## 🎯 Naming Convention

- **API**: `camelCase` (birthDate, accountType, isActive)
- **БД**: `snake_case` (birth_date, account_type, is_active)

---

## 📞 Swagger UI

Интерактивная документация:
```
http://localhost:8000/docs
```

Можно тестировать все эндпоинты прямо в браузере!

---

**Backend готов! Все данные реальные из банков VBank, ABank, SBank!** 🚀
