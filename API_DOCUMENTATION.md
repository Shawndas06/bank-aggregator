# 📚 API Documentation для Frontend разработчика

## Base URL
```
http://localhost:8000
```

## Формат ответов

### ✅ Успешный ответ
```json
{
  "success": true,
  "data": { ... }
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
```
POST /api/auth/sign-up
```

**Body:**
```json
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

**Примечание:** `otpCode` возвращается только в режиме разработки.

---

### 2. Подтверждение Email
```
POST /api/auth/verify-email
```

**Body:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Email подтверждён! Вы автоматически вошли в систему.",
    "user": {
      "id": 1,
      "name": "Иван Иванов",
      "birthDate": "2000-01-01",
      "accountType": "free"
    }
  }
}
```

**Cookie:** Устанавливается `session-id` (httpOnly)

---

### 3. Вход
```
POST /api/auth/sign-in
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

**Response (200):**
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

**Cookie:** Устанавливается `session-id` (httpOnly)

**Ошибки:**
- 401: Неверный email или пароль
- 403: Аккаунт не подтверждён

---

### 4. Текущий пользователь
```
GET /api/auth/me
```

**Headers:**
```
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
```
POST /api/auth/logout
```

**Headers:**
```
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
```
GET /api/accounts
GET /api/accounts?client_id=1
```

**Headers:**
```
Cookie: session-id=...
```

**Query params:**
- `client_id` (optional): ID банка для фильтрации (1=VBank, 2=SBank, 3=ABank)

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "accountId": "vbank_acc_001",
      "accountName": "Основной счёт",
      "clientId": 1,
      "clientName": "vbank",
      "isActive": true
    }
  ]
}
```

---

### 2. Создать счёт
```
POST /api/accounts
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
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
      "accountId": "vbank_acc_001",
      "accountName": "Основной счёт",
      "clientId": 1,
      "isActive": true
    }
  }
}
```

---

### 3. Привязать счёт
```
POST /api/accounts/attach
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
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
```
GET /api/accounts/{account_id}?client_id=1
```

**Headers:**
```
Cookie: session-id=...
```

**Path params:**
- `account_id`: ID счёта

**Query params:**
- `client_id`: ID банка (обязательно)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "accountId": "vbank_acc_001",
    "accountName": "Основной счёт",
    "clientId": 1,
    "clientName": "vbank",
    "isActive": true
  }
}
```

---

### 5. Баланс счёта
```
GET /api/accounts/{account_id}/balances?client_id=1
```

**Headers:**
```
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "amount": 1500.50,
    "currency": "EUR"
  }
}
```

---

### 6. Транзакции счёта
```
GET /api/accounts/{account_id}/transactions?client_id=1
```

**Headers:**
```
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "txn_12345",
      "date": "2024-11-08T10:30:00",
      "description": "Покупка в магазине",
      "amount": -50.00,
      "currency": "EUR",
      "type": "debit"
    }
  ]
}
```

---

## 👥 Группы

### 1. Список групп
```
GET /api/groups
```

**Headers:**
```
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
      "createdAt": "2024-11-08T10:00:00"
    }
  ]
}
```

---

### 2. Создать группу
```
POST /api/groups
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
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
    "createdAt": "2024-11-08T10:00:00"
  }
}
```

**Ошибки:**
- 400: Достигнут лимит групп (1 для free, 5 для premium)

---

### 3. Настройки групп
```
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

### 4. Удалить группу
```
DELETE /api/groups
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
{
  "groupId": 1
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Группа успешно удалена"
  }
}
```

**Ошибки:**
- 400: Только владелец может удалить группу

---

### 5. Выйти из группы
```
POST /api/groups/exit
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
{
  "groupId": 1
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Вы успешно вышли из группы"
  }
}
```

**Ошибки:**
- 400: Владелец не может выйти из группы

---

### 6. Счета группы
```
GET /api/groups/{group_id}/accounts
```

**Headers:**
```
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
      "accountId": "vbank_acc_001",
      "accountName": "Основной счёт"
    }
  ]
}
```

---

### 7. Балансы группы
```
GET /api/groups/{group_id}/accounts/balances
GET /api/groups/{group_id}/accounts/balances?client_id=1
```

**Headers:**
```
Cookie: session-id=...
```

**Query params:**
- `client_id` (optional): Фильтр по банку

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "clientId": "1",
      "name": "vbank",
      "accountName": "Основной счёт",
      "owner": {
        "name": "Иван"
      },
      "balance": {
        "amount": 1200.50,
        "currency": "EUR"
      }
    }
  ]
}
```

---

### 8. Транзакции группы
```
GET /api/groups/{group_id}/accounts/transactions
GET /api/groups/{group_id}/accounts/transactions?client_id=1
```

**Headers:**
```
Cookie: session-id=...
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "txn_12345",
      "date": "2024-11-08T10:30:00",
      "description": "Покупка",
      "amount": -50.00,
      "currency": "EUR",
      "type": "debit",
      "owner": {
        "name": "Иван"
      },
      "accountName": "Основной счёт"
    }
  ]
}
```

---

### 9. Пригласить в группу
```
POST /api/groups/invite
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
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

**Ошибки:**
- 400: Пользователь не найден
- 400: Пользователь уже в группе
- 400: Достигнут лимит членов

---

### 10. Принять приглашение
```
POST /api/groups/invite/accept
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
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

### 11. Отклонить приглашение
```
POST /api/groups/invite/decline
```

**Headers:**
```
Cookie: session-id=...
```

**Body:**
```json
{
  "request_id": 1
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "message": "Приглашение отклонено"
  }
}
```

---

## 🏦 Банки

### Список доступных банков

| ID | Название | Код |
|----|----------|-----|
| 1  | VBank    | vbank |
| 2  | SBank    | sbank |
| 3  | ABank    | abank |

---

## 🍪 Работа с Cookie

### Frontend (JavaScript/Fetch)
```javascript
fetch('http://localhost:8000/api/auth/me', {
  credentials: 'include'  // ВАЖНО!
})
```

### Frontend (Axios)
```javascript
axios.defaults.withCredentials = true;
```

---

## ⚠️ Важные моменты

1. **Все защищённые эндпоинты требуют cookie `session-id`**
   - Устанавливается автоматически после `/sign-in` или `/verify-email`
   - Время жизни: 24 часа

2. **Naming convention**
   - API использует `camelCase` для полей
   - Примеры: `birthDate`, `accountType`, `isActive`

3. **Mock данные**
   - Все банковские данные (счета, балансы, транзакции) - mock
   - Достаточно для полноценной разработки Frontend

4. **Кеширование**
   - Балансы и транзакции кешируются на 4 часа
   - Повторные запросы возвращают кешированные данные

5. **Лимиты Free аккаунта**
   - 1 группа
   - 2 члена в группе

6. **CORS**
   - Разрешены origins: `localhost:3000`, `localhost:5173`, `localhost:8080`

---

## 📞 Тестирование через curl

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456","name":"Test","birthDate":"2000-01-01"}'

# Вход (получаем cookie)
curl -X POST http://localhost:8000/api/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}' \
  -c cookies.txt

# Список счетов (используем cookie)
curl http://localhost:8000/api/accounts \
  -b cookies.txt
```

---

**Backend готов! Swagger UI: http://localhost:8000/docs** 🚀

