#!/bin/bash

# Скрипт для развертывания на сервере
# Выполните этот скрипт на сервере после копирования проекта

set -e

echo "🚀 Начало развертывания Bank Aggregator..."

# === Установка зависимостей ===
echo "📦 Установка зависимостей..."

apt-get update -y
apt-get install -y curl git

# Docker
if ! command -v docker &> /dev/null; then
    echo "Установка Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    rm get-docker.sh
else
    echo "✅ Docker уже установлен: $(docker --version)"
fi

# Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Установка Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
else
    echo "✅ Docker Compose уже установлен: $(docker-compose --version)"
fi

# Node.js
if ! command -v node &> /dev/null; then
    echo "Установка Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
else
    echo "✅ Node.js уже установлен: $(node --version)"
fi

# Nginx
if ! command -v nginx &> /dev/null; then
    echo "Установка Nginx..."
    apt-get install -y nginx
    systemctl start nginx
    systemctl enable nginx
else
    echo "✅ Nginx уже установлен"
fi

echo "✅ Зависимости установлены"
echo ""

# === Проверка структуры проекта ===
PROJECT_DIR="/root/bank-aggregator"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Проект не найден в $PROJECT_DIR"
    echo "Сначала скопируйте проект на сервер (см. QUICK_DEPLOY.md)"
    exit 1
fi

cd $PROJECT_DIR

# === Настройка Backend ===
echo "⚙️ Настройка Backend..."

cd backend

# Обновление ALLOWED_ORIGINS
if [ -f "docker-compose.yaml" ]; then
    echo "Обновление конфигурации Backend..."
    sed -i 's|ALLOWED_ORIGINS.*|ALLOWED_ORIGINS=http://147.45.253.75,http://147.45.253.75:5173,http://localhost:5173,http://localhost:3000|g' docker-compose.yaml || true
fi

# Запуск Backend
echo "Запуск Backend сервисов..."
docker-compose down 2>/dev/null || true
docker-compose up -d --build

echo "Ожидание запуска сервисов..."
sleep 15

# Проверка статуса
echo "Проверка статуса Backend..."
docker-compose ps

# Проверка health
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend запущен и работает"
else
    echo "⚠️ Backend запускается, проверьте логи: docker-compose logs -f backend"
fi

echo ""

# === Настройка Frontend ===
echo "⚙️ Настройка Frontend..."

cd ../frontend

# Установка зависимостей
echo "Установка зависимостей Frontend..."
npm install

# Сборка production
echo "Сборка production версии..."
npm run build

if [ -d "dist" ]; then
    echo "✅ Frontend собран"
else
    echo "❌ Ошибка сборки Frontend"
    exit 1
fi

echo ""

# === Настройка Nginx ===
echo "⚙️ Настройка Nginx..."

cat > /etc/nginx/sites-available/bank-aggregator << 'NGINX_CONFIG'
server {
    listen 80;
    server_name 147.45.253.75;
    
    root /root/bank-aggregator/frontend/dist;
    index index.html;
    
    # Frontend (React SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Backend docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /health {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
    
    location /openapi.json {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
NGINX_CONFIG

# Активация конфигурации
ln -sf /etc/nginx/sites-available/bank-aggregator /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации
if nginx -t; then
    echo "✅ Конфигурация Nginx корректна"
    systemctl restart nginx
    echo "✅ Nginx перезапущен"
else
    echo "❌ Ошибка в конфигурации Nginx"
    exit 1
fi

echo ""

# === Настройка файрвола ===
echo "🔒 Настройка файрвола..."

ufw allow 80/tcp 2>/dev/null || true
ufw allow 443/tcp 2>/dev/null || true
ufw allow 8000/tcp 2>/dev/null || true
ufw --force enable 2>/dev/null || true

echo "✅ Порты открыты"
echo ""

# === Итоговая проверка ===
echo "=== Проверка сервисов ==="
echo ""
echo "Backend:"
docker-compose ps
echo ""
echo "Nginx:"
systemctl status nginx --no-pager | head -5
echo ""
echo "Проверка доступности:"
curl -s http://localhost:8000/health | head -5 || echo "Backend еще запускается..."
echo ""

# === Результат ===
echo "========================================="
echo "✅ РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО!"
echo "========================================="
echo ""
echo "🌐 Ваше приложение доступно по адресу:"
echo "   http://147.45.253.75"
echo ""
echo "📊 API документация:"
echo "   http://147.45.253.75/docs"
echo ""
echo "💚 Health Check:"
echo "   http://147.45.253.75/health"
echo ""
echo "📱 URL для QR-кода презентации:"
echo "   http://147.45.253.75"
echo ""
echo "========================================="

