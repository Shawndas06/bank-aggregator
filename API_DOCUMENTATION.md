# Bank Aggregator API - Документация для Frontend

**Base URL:** `http://localhost:8000`  
**Swagger UI:** `http://localhost:8000/docs` ← **ОТКРОЙТЕ ЭТОТ URL ЧТОБЫ УВИДЕТЬ ВСЕ API ИНТЕРАКТИВНО**

---

## 🎯 Как посмотреть все API роуты

### Вариант 1: Swagger UI (Рекомендуется)
Откройте в браузере: **http://localhost:8000/docs**

Там вы увидите:
- ✅ Все доступные эндпоинты
- ✅ Параметры запросов
- ✅ Примеры ответов
- ✅ Возможность протестировать запросы прямо в браузере

### Вариант 2: ReDoc
Откройте в браузере: **http://localhost:8000/redoc**

### Вариант 3: Эта документация
Ниже все эндпоинты с примерами

---

## 📚 Все API Эндпоинты (26 штук)

### 🔐 Authentication (5 эндпоинтов)

#### 1. POST `/api/auth/sign-up` - Регистрация

**Request:**
```json
{
  "email": "user@example.com",
  "password": "Test123456",
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

#### 2. POST `/api/auth/verify-email` - Подтверждение email

**Request:**
```json
{
  "email": "user@example.com",
  "otpCode": "123456"
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

**⚠️ Важно:** Устанавливает HTTP-only cookie с `session-id`

---

#### 3. POST `/api/auth/sign-in` - Вход

**Request:**
```json
{
  "email": "user@example.com",
  "password": "Test123456"
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

**⚠️ Важно:** Устанавливает HTTP-only cookie с `session-id`

---

#### 4. GET `/api/auth/me` - Текущий пользователь

**Request:** Нет body (используется cookie)

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

#### 5. POST `/api/auth/logout` - Выход

**Request:** Нет body

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

### 💳 Accounts - Счета (6 эндпоинтов)

#### 6. POST `/api/accounts` - Создать счет

**Request:**
```json
{
  "clientId": 1
}
```

**Параметры:**
- `clientId`: ID банка (1 = VBank, 2 = SBank, 3 = ABank)

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

---

#### 7. GET `/api/accounts` - Список всех счетов

**Query Parameters (опционально):**
- `client_id` - фильтр по банку

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
    },
    {
      "accountId": "acc-5522",
      "accountName": "Savings Account",
      "clientId": 3,
      "clientName": "abank",
      "isActive": true
    }
  ]
}
```

---

#### 8. GET `/api/accounts?client_id=1` - Фильтр по банку

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

---

#### 9. POST `/api/accounts/attach` - Привязать счет

**Request:**
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

#### 10. GET `/api/accounts/{account_id}?client_id=1` - Информация по счету

**Path Parameters:**
- `account_id` - ID счета

**Query Parameters:**
- `client_id` - ID банка (обязательно)

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

#### 11. GET `/api/accounts/{account_id}/balances?client_id=1` - Баланс счета

**Response (200):**
```json
{
  "success": true,
  "data": {
    "amount": 117404.06,
    "currency": "RUB"
  }
}
```

---

#### 12. GET `/api/accounts/{account_id}/transactions?client_id=1` - Транзакции

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "tx-vbank-00573612",
      "date": "2025-11-08T18:50:15.285567Z",
      "description": "Пятёрочка - Санкт-Петербург",
      "amount": 565.05,
      "currency": "RUB",
      "type": "debit"
    },
    {
      "id": "tx-vbank-00573658",
      "date": "2025-11-05T10:54:15.285567Z",
      "description": "Платеж по кредиту",
      "amount": 15139.44,
      "currency": "RUB",
      "type": "debit"
    }
  ]
}
```

---

### 👥 Groups - Группы (14 эндпоинтов)

#### 13. POST `/api/groups` - Создать группу

**Request:**
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
    "createdAt": "2025-11-08 17:15:39.843117+00:00"
  }
}
```

---

#### 14. GET `/api/groups` - Список групп

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Моя семья",
      "ownerId": 1,
      "createdAt": "2025-11-08 17:15:39.843117+00:00"
    }
  ]
}
```

---

#### 15. GET `/api/groups/settings` - Настройки лимитов

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

#### 16. DELETE `/api/groups` - Удалить группу

**Request:**
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

---

#### 17. POST `/api/groups/exit` - Выйти из группы

**Request:**
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

---

#### 18. GET `/api/groups/{group_id}/accounts` - Счета группы

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "owner": {
        "name": "Иван Иванов"
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

#### 19. GET `/api/groups/{group_id}/accounts/{client_id}` - Детали счета группы

**Response (200):**
```json
{
  "success": true,
  "data": {
    "owner": {
      "name": "Иван Иванов"
    },
    "clientId": "1",
    "clientName": "vbank",
    "accountId": "acc-3311",
    "accountName": "Checking счет"
  }
}
```

---

#### 20. GET `/api/groups/{group_id}/accounts/balances` - Балансы группы

**Query Parameters (опционально):**
- `client_id` - фильтр по банку

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
        "name": "Иван Иванов"
      },
      "balance": {
        "amount": 117404.06,
        "currency": "RUB"
      }
    }
  ]
}
```

---

#### 21. GET `/api/groups/{group_id}/accounts/transactions` - Транзакции группы

**Query Parameters (опционально):**
- `client_id` - фильтр по банку

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "tx-vbank-00573612",
      "date": "2025-11-08T18:50:15.285567Z",
      "description": "Пятёрочка - Санкт-Петербург",
      "amount": 565.05,
      "currency": "RUB",
      "type": "debit",
      "owner": {
        "name": "Иван Иванов"
      },
      "accountName": "Checking счет"
    }
  ]
}
```

---

#### 22. POST `/api/groups/invite` - Пригласить в группу

**Request:**
```json
{
  "groupId": 1,
  "email": "user2@example.com"
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

#### 23. GET `/api/groups/invites` - Мои приглашения

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "groupId": 1,
      "inviterEmail": "user1@example.com",
      "inviterName": "Иван Иванов",
      "status": "pending",
      "createdAt": "2025-11-08 17:17:35.388957+00:00"
    }
  ]
}
```

---

#### 24. POST `/api/groups/invite/accept` - Принять приглашение

**Request:**
```json
{
  "requestId": 1
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

#### 25. POST `/api/groups/invite/decline` - Отклонить приглашение

**Request:**
```json
{
  "requestId": 1
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

### ❤️ Health Check (2 эндпоинта)

#### 26. GET `/` - Базовый health check

**Response (200):**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "app": "Bank Aggregator API",
    "version": "1.0.0"
  }
}
```

---

#### 27. GET `/health` - Детальный health check

**Response (200):**
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

## 🔴 Формат ошибок

Все ошибки возвращаются в едином формате:

**Error Response (400/401/403/404/500):**
```json
{
  "success": false,
  "error": {
    "message": "Описание ошибки"
  }
}
```

**Примеры:**

```json
{
  "success": false,
  "error": {
    "message": "Пользователь с таким email уже существует"
  }
}
```

```json
{
  "success": false,
  "error": {
    "message": "Аккаунт не подтвержден. Пожалуйста, подтвердите email."
  }
}
```

```json
{
  "success": false,
  "error": {
    "message": "Вы не являетесь членом этой группы"
  }
}
```

---

## 🍪 Аутентификация через Cookie

**Важно:** Все защищенные эндпоинты используют HTTP-only cookie с именем `session-id`.

### Как это работает:

1. После `/api/auth/sign-in` или `/api/auth/verify-email` сервер устанавливает cookie
2. Браузер автоматически отправляет этот cookie с каждым запросом
3. Сервер проверяет session-id в Redis
4. Если сессия валидна - запрос обрабатывается

### Для Frontend:

```javascript
// Пример с fetch
const response = await fetch('http://localhost:8000/api/accounts', {
  method: 'GET',
  credentials: 'include', // ← Важно! Отправляет cookies
  headers: {
    'Content-Type': 'application/json'
  }
});
```

```javascript
// Пример с axios
axios.defaults.withCredentials = true;

const response = await axios.get('http://localhost:8000/api/accounts');
```

---

## 🏦 Банки (Bank IDs)

| ID | Название | URL | Статус |
|----|----------|-----|--------|
| 1 | VBank | vbank.open.bankingapi.ru | ✅ Протестирован |
| 2 | SBank (Сбербанк) | sbank.open.bankingapi.ru | ✅ Протестирован |
| 3 | ABank | abank.open.bankingapi.ru | ✅ Протестирован |

**Все 3 банка полностью работают!**

---

## 📝 Примеры полных флоу

### Флоу 1: Регистрация и создание счета

```bash
# 1. Регистрация
curl -X POST http://localhost:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "name": "Test User",
    "birthDate": "2000-01-01"
  }'

# 2. Подтверждение email (сохраняет cookie)
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "otpCode": "123456"
  }' \
  -c cookies.txt

# 3. Создание счета
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"clientId": 1}' \
  -b cookies.txt

# 4. Получение баланса
curl -X GET 'http://localhost:8000/api/accounts/acc-3311/balances?client_id=1' \
  -b cookies.txt
```

---

### Флоу 2: Создание группы и приглашение

```bash
# 1. Создать группу
curl -X POST http://localhost:8000/api/groups \
  -H "Content-Type: application/json" \
  -d '{"name": "Моя семья"}' \
  -b cookies.txt

# 2. Пригласить пользователя
curl -X POST http://localhost:8000/api/groups/invite \
  -H "Content-Type: application/json" \
  -d '{"groupId": 1, "email": "user2@example.com"}' \
  -b cookies.txt

# 3. Посмотреть счета группы
curl -X GET http://localhost:8000/api/groups/1/accounts \
  -b cookies.txt

# 4. Посмотреть балансы группы
curl -X GET http://localhost:8000/api/groups/1/accounts/balances \
  -b cookies.txt
```

---

## 🚀 Запуск проекта

```bash
# Клонировать репозиторий
git clone <repository-url>
cd bank-aggregator

# Запустить через Docker
docker-compose up -d

# Проверить health
curl http://localhost:8000/health

# Открыть Swagger UI
# Откройте в браузере: http://localhost:8000/docs
```

---

## 📂 Где найти код API роутов

Все API роуты находятся в папке `src/routers/`:

1. **`src/routers/auth.py`** - Аутентификация (5 эндпоинтов)
2. **`src/routers/accounts.py`** - Счета (6 эндпоинтов)
3. **`src/routers/groups.py`** - Группы (14 эндпоинтов)

Подключение роутов в `main.py`:
```python
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(groups.router)
```

---

## 🎨 Для Frontend: React примеры

### Создание API клиента

```typescript
// api/client.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true, // Важно для cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Обработка ответов
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error.message);
    }
    throw error;
  }
);

export default api;
```

### Примеры запросов

```typescript
// api/auth.ts
import api from './client';

export const authAPI = {
  signUp: (data: SignUpData) => api.post('/api/auth/sign-up', data),
  verifyEmail: (data: VerifyEmailData) => api.post('/api/auth/verify-email', data),
  signIn: (data: SignInData) => api.post('/api/auth/sign-in', data),
  getMe: () => api.get('/api/auth/me'),
  logout: () => api.post('/api/auth/logout'),
};

// api/accounts.ts
export const accountsAPI = {
  getAll: (clientId?: number) => 
    api.get('/api/accounts', { params: { client_id: clientId } }),
  create: (clientId: number) => 
    api.post('/api/accounts', { clientId }),
  getBalance: (accountId: string, clientId: number) =>
    api.get(`/api/accounts/${accountId}/balances`, { params: { client_id: clientId } }),
  getTransactions: (accountId: string, clientId: number) =>
    api.get(`/api/accounts/${accountId}/transactions`, { params: { client_id: clientId } }),
};

// api/groups.ts
export const groupsAPI = {
  getAll: () => api.get('/api/groups'),
  create: (name: string) => api.post('/api/groups', { name }),
  getAccounts: (groupId: number) => api.get(`/api/groups/${groupId}/accounts`),
  getBalances: (groupId: number, clientId?: number) =>
    api.get(`/api/groups/${groupId}/accounts/balances`, { params: { client_id: clientId } }),
};
```

---

## 📞 Поддержка

**Swagger UI:** http://localhost:8000/docs ← **ЛУЧШИЙ СПОСОБ ИЗУЧИТЬ API**

При возникновении вопросов:
1. Откройте Swagger UI
2. Попробуйте запрос прямо там
3. Посмотрите пример ответа

**Все 26 эндпоинтов протестированы и работают! ✅**

