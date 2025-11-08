# 🏦 Bank Aggregator API

**Монолитное приложение для агрегации банковских счетов с поддержкой групп**

Проект для хакатона VTB API 2025 - Кейс "Мультибанк"

---

## 🚀 Быстрый старт (Docker Compose)

```bash
# Запуск всего проекта (Backend + PostgreSQL + Redis)
docker-compose up -d

# Просмотр логов
docker-compose logs -f backend

# Остановка
docker-compose down
```

**API:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs

---

## 🔑 Credentials (VTB Hackathon 2025)

```
Team ID:     team222
Team Secret: Wl1F0L2aVHOPE20rM0DFeqvP9Qr2pgQT
```

✅ Уже настроены в `docker-compose.yaml`

---

## 📦 Что включено в Docker Compose

```yaml
services:
  backend:    # FastAPI приложение (порт 8000)
  postgres:   # PostgreSQL база данных (порт 5432)
  redis:      # Redis кеш (порт 6379)
```

**Volumes (данные сохраняются между перезапусками):**
- `postgres_data` - данные PostgreSQL
- `redis_data` - данные Redis

**Network:**
- `bank_network` - внутренняя сеть для общения между контейнерами

---

## 🏗️ Архитектура

**Монолитная архитектура на FastAPI**

```
bank-aggregator/
├── Dockerfile              # Docker образ для backend
├── docker-compose.yaml     # Оркестрация всех сервисов
├── .dockerignore          # Исключения для Docker
├── main.py                # Точка входа
├── init_db.py            # Инициализация БД
├── test_bank_api.py      # Тестирование интеграции
├── requirements.txt
├── .env                  # Настройки (НЕ используется в Docker!)
├── README.md             # Эта документация
├── API_DOCUMENTATION.md  # Для Frontend разработчика
└── src/                  # Исходный код
    ├── models/           # 6 моделей БД
    ├── routers/          # 3 роутера (25 эндпоинтов)
    ├── services/         # 7 сервисов
    ├── schemas/          # Pydantic схемы
    ├── utils/            # Утилиты
    └── constants/        # Константы
```

---

## 📋 API Эндпоинты (25 штук)

### 🔐 Аутентификация (5)

```
POST   /api/auth/sign-up          Регистрация
POST   /api/auth/verify-email     Подтверждение (OTP: 123456)
POST   /api/auth/sign-in          Вход (session-id cookie)
GET    /api/auth/me               Текущий пользователь
POST   /api/auth/logout           Выход
```

### 💳 Счета (6)

```
GET    /api/accounts                      Список счетов
GET    /api/accounts?client_id=1          Фильтр по банку
POST   /api/accounts                      Создать счёт
POST   /api/accounts/attach               Привязать счёт
GET    /api/accounts/{id}?client_id=1     Информация о счёте
GET    /api/accounts/{id}/balances?client_id=1    Баланс (реальный!)
GET    /api/accounts/{id}/transactions?client_id=1 Транзакции (реальные!)
```

### 👥 Группы (14)

```
POST   /api/groups                        Создать группу
GET    /api/groups                        Список групп
GET    /api/groups/settings               Лимиты
DELETE /api/groups                        Удалить группу
POST   /api/groups/exit                   Выйти из группы
POST   /api/groups/invite                 Пригласить
POST   /api/groups/invite/accept          Принять приглашение
POST   /api/groups/invite/decline         Отклонить приглашение
GET    /api/groups/{id}/accounts          Счета группы
GET    /api/groups/{id}/accounts/balances Балансы группы
GET    /api/groups/{id}/accounts/transactions Транзакции группы
```

**Полная документация:** `API_DOCUMENTATION.md`

---

## 🏦 Интеграция с банками

Backend интегрирован с **реальным OpenBanking API**:

| Банк | URL | ID | Статус |
|------|-----|-----|--------|
| VBank | vbank.open.bankingapi.ru | 1 | ✅ Работает |
| ABank | abank.open.bankingapi.ru | 3 | ✅ Работает |
| SBank | sbank.open.bankingapi.ru | 2 | ⚠️ Требует подтверждения |

**Как это работает:**
1. Получение токена банка (POST /auth/bank-token) → кеш 23ч
2. Создание consent (POST /account-consents/request) → кеш 4ч
3. Запрос данных (GET /accounts, /balances, /transactions) → кеш 4ч

**Все данные реальные из банков!**

---

## 📊 Формат ответов

### Успех
```json
{
  "success": true,
  "data": {...}
}
```

### Ошибка
```json
{
  "success": false,
  "error": {
    "message": "Описание ошибки"
  }
}
```

**Naming:** camelCase (birthDate, accountType, isActive)

---

## 🐳 Docker Compose команды

### Основные команды:

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка
docker-compose down

# Остановка с удалением volumes (данные будут удалены!)
docker-compose down -v

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis

# Перезапуск сервиса
docker-compose restart backend

# Пересборка образа
docker-compose build backend

# Запуск с пересборкой
docker-compose up -d --build
```

### Инициализация БД:

```bash
# После первого запуска
docker-compose exec backend python init_db.py
```

### Проверка работы:

```bash
# Health check
curl http://localhost:8000/health

# Или
docker-compose exec backend curl http://localhost:8000/health
```

---

## 🧪 Тестирование

### Тест интеграции с банками:

```bash
# Внутри контейнера
docker-compose exec backend python test_bank_api.py

# Или локально (если есть Python)
python3 test_bank_api.py
```

### Через Swagger UI:

```
http://localhost:8000/docs
```

### Через curl:

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123456","name":"Test User","birthDate":"2000-01-01"}'

# Подтверждение (OTP: 123456)
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","code":"123456"}' \
  -c cookies.txt

# Создание счёта (РЕАЛЬНЫЕ ДАННЫЕ из VBank!)
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"client_id":1}' \
  -b cookies.txt
```

---

## 🔧 Разработка без Docker

Если нужно запустить локально (без Docker):

```bash
# 1. Установка зависимостей
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Запуск PostgreSQL и Redis
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bank_aggregator postgres:15
docker run -d --name redis -p 6379:6379 redis:7

# 3. Обновить src/config.py
# DATABASE_HOST: str = "localhost"
# REDIS_HOST: str = "localhost"

# 4. Инициализация БД
python3 init_db.py

# 5. Запуск
python3 main.py
```

---

## 📚 Документация

### Для команды:
- **README.md** - эта документация (всё что нужно знать о проекте)

### Для Frontend:
- **API_DOCUMENTATION.md** - все эндпоинты с примерами
- **Swagger UI** - http://localhost:8000/docs (интерактивная)

---

## 🔐 Безопасность

- ✅ Пароли хешируются (bcrypt)
- ✅ HTTP-only cookie для сессий
- ✅ JWT токены от банков (RS256/HS256)
- ✅ Consents для межбанкового доступа
- ✅ Валидация данных (Pydantic)
- ✅ CORS настроен

---

## 📦 Модели данных

**6 моделей БД:**
- `User` - пользователи
- `OTPCode` - коды подтверждения
- `BankAccount` - банковские счета
- `Group` - группы
- `GroupMember` - членство
- `Invitation` - приглашения

**Лимиты:**
- **Free**: 1 группа, 2 члена
- **Premium**: 5 групп, 20 членов

---

## 📊 Кеширование в Redis

| Что | Ключ | TTL |
|-----|------|-----|
| Токен банка | `bank_token:{user_id}:{bank_id}` | 23ч |
| Consent | `consent:{user_id}:{bank_id}` | 4ч |
| Баланс | `balance:{user_id}:{account_id}` | 4ч |
| Транзакции | `transactions:{user_id}:{account_id}` | 4ч |
| Сессия | `session:{session_id}` | 24ч |

---

## 🚨 Troubleshooting

### Контейнеры не запускаются?

```bash
# Проверка статуса
docker-compose ps

# Логи
docker-compose logs backend
docker-compose logs postgres
docker-compose logs redis
```

### Backend показывает ошибку подключения к БД?

```bash
# Проверьте что postgres готов
docker-compose exec postgres pg_isready -U postgres

# Пересоздайте БД
docker-compose exec backend python init_db.py
```

### Нужно очистить все данные?

```bash
# Остановить и удалить volumes
docker-compose down -v

# Запустить заново
docker-compose up -d

# Инициализировать БД
docker-compose exec backend python init_db.py
```

### Изменили код и нужно пересобрать?

```bash
# Пересборка и перезапуск
docker-compose up -d --build
```

---

## 🛠️ Технологии

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - База данных
- **Redis** - Кеширование и сессии
- **Pydantic** - Валидация
- **httpx** - HTTP клиент для банков
- **bcrypt** - Хеширование паролей
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация

---

## 👥 Команда

**Хакатон:** VTB API 2025 - Кейс "Мультибанк"  
**Команда:** team222  
**Разработчики:**
- Baga - Аутентификация, сессии, OTP
- Ezira - Счета, банковская интеграция, группы

---

## ✅ Статус проекта

✅ **25 эндпоинтов** реализованы  
✅ **Интеграция с VBank и ABank** работает (реальное OpenBanking API)  
✅ **Кеширование** настроено  
✅ **Docker Compose** готов  
✅ **Документация** полная  
✅ **Готов к production** 🚀

---

## 🎯 Для Frontend разработчика

### Base URL
```
http://localhost:8000
```

### Cookie аутентификация
```javascript
fetch('http://localhost:8000/api/auth/me', {
  credentials: 'include'
})
```

### Swagger UI (интерактивная документация)
```
http://localhost:8000/docs
```

### Полная документация
```
API_DOCUMENTATION.md
```

---

**Backend готов! Frontend может начинать интеграцию!** 🎉
