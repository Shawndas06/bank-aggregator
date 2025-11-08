#!/bin/bash

# Скрипт быстрого запуска Backend

echo "🚀 Запуск Bank Aggregator Backend..."

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Создайте его: python3 -m venv venv"
    exit 1
fi

# Активация виртуального окружения
source venv/bin/activate

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден! Создаём из примера..."
    cp .env.example .env 2>/dev/null || echo "❌ Файл .env.example не найден!"
fi

# Проверка PostgreSQL
echo "🔍 Проверка PostgreSQL..."
if ! docker ps | grep -q postgres; then
    echo "⚠️  PostgreSQL не запущен. Запускаем..."
    docker run -d \
        --name postgres \
        -e POSTGRES_PASSWORD=password \
        -e POSTGRES_DB=bank_aggregator \
        -p 5432:5432 \
        postgres:15
    sleep 3
fi

# Проверка Redis
echo "🔍 Проверка Redis..."
if ! docker ps | grep -q redis; then
    echo "⚠️  Redis не запущен. Запускаем..."
    docker run -d \
        --name redis \
        -p 6379:6379 \
        redis:7
    sleep 2
fi

# Инициализация БД (если нужно)
echo "📊 Инициализация БД..."
python init_db.py

# Запуск сервера
echo "✨ Запуск сервера на http://localhost:8000"
echo "📚 Swagger UI: http://localhost:8000/docs"
echo ""
python main.py

