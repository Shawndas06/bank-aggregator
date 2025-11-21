#!/bin/bash

# Скрипт для развертывания Bank Aggregator на облачном сервере
# Использование: ./deploy.sh

set -e

echo "🚀 Начало развертывания Bank Aggregator..."

# Переменные
SERVER_IP="147.45.253.75"
SERVER_USER="root"
SERVER_PASS="dmFMG+JPE6whwv"
PROJECT_DIR="/root/bank-aggregator"

echo "📦 Шаг 1: Подключение к серверу и установка зависимостей..."

ssh -o StrictHostKeyChecking=no root@${SERVER_IP} << 'ENDSSH'
    echo "=== Проверка и установка зависимостей ==="
    
    # Обновление системы
    apt-get update -y
    
    # Установка Docker
    if ! command -v docker &> /dev/null; then
        echo "Установка Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl start docker
        systemctl enable docker
        rm get-docker.sh
    else
        echo "Docker уже установлен: $(docker --version)"
    fi
    
    # Установка Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "Установка Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
    else
        echo "Docker Compose уже установлен: $(docker-compose --version)"
    fi
    
    # Установка Node.js 18+
    if ! command -v node &> /dev/null; then
        echo "Установка Node.js..."
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt-get install -y nodejs
    else
        echo "Node.js уже установлен: $(node --version)"
    fi
    
    # Установка Nginx
    if ! command -v nginx &> /dev/null; then
        echo "Установка Nginx..."
        apt-get install -y nginx
        systemctl start nginx
        systemctl enable nginx
    else
        echo "Nginx уже установлен"
    fi
    
    echo "✅ Зависимости установлены"
ENDSSH

echo "📤 Шаг 2: Копирование проекта на сервер..."

# Создание архива проекта (исключая node_modules и другие ненужные файлы)
cd /home/baga/Desktop/Ezira/bank-aggregator
tar --exclude='node_modules' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='dist' \
    --exclude='build' \
    -czf /tmp/bank-aggregator.tar.gz .

# Копирование на сервер
echo "Копирование файлов..."
sshpass -p "${SERVER_PASS}" scp -o StrictHostKeyChecking=no /tmp/bank-aggregator.tar.gz root@${SERVER_IP}:/tmp/

# Распаковка на сервере
ssh -o StrictHostKeyChecking=no root@${SERVER_IP} << ENDSSH
    mkdir -p ${PROJECT_DIR}
    cd ${PROJECT_DIR}
    tar -xzf /tmp/bank-aggregator.tar.gz
    rm /tmp/bank-aggregator.tar.gz
    echo "✅ Проект распакован"
ENDSSH

echo "⚙️ Шаг 3: Настройка проекта на сервере..."

ssh -o StrictHostKeyChecking=no root@${SERVER_IP} << ENDSSH
    cd ${PROJECT_DIR}
    
    echo "=== Настройка Backend ==="
    cd backend
    
    # Обновление ALLOWED_ORIGINS для production
    sed -i "s|ALLOWED_ORIGINS.*|ALLOWED_ORIGINS=http://147.45.253.75,http://147.45.253.75:5173,http://localhost:5173,http://localhost:3000|g" docker-compose.yaml || true
    
    # Запуск Backend
    echo "Запуск Backend сервисов..."
    docker-compose down 2>/dev/null || true
    docker-compose up -d --build
    
    echo "Ожидание запуска сервисов..."
    sleep 10
    
    # Проверка статуса
    docker-compose ps
    
    echo "=== Настройка Frontend ==="
    cd ../frontend
    
    # Установка зависимостей
    echo "Установка зависимостей frontend..."
    npm install
    
    # Сборка production версии
    echo "Сборка production версии..."
    npm run build
    
    echo "=== Настройка Nginx ==="
    
    # Создание конфигурации Nginx для frontend
    cat > /etc/nginx/sites-available/bank-aggregator << 'NGINX_CONFIG'
server {
    listen 80;
    server_name 147.45.253.75;
    
    root /root/bank-aggregator/frontend/dist;
    index index.html;
    
    # Frontend (React SPA)
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # Backend API proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Backend docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
    
    location /health {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
    }
}
NGINX_CONFIG

    # Активация конфигурации
    ln -sf /etc/nginx/sites-available/bank-aggregator /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Проверка конфигурации Nginx
    nginx -t
    
    # Перезапуск Nginx
    systemctl restart nginx
    
    echo "=== Настройка файрвола ==="
    
    # Открытие портов
    ufw allow 80/tcp || true
    ufw allow 443/tcp || true
    ufw allow 8000/tcp || true
    ufw allow 5173/tcp || true
    ufw --force enable || true
    
    echo "✅ Настройка завершена"
    
    echo ""
    echo "=== Статус сервисов ==="
    echo "Backend:"
    cd ${PROJECT_DIR}/backend
    docker-compose ps
    
    echo ""
    echo "Nginx:"
    systemctl status nginx --no-pager | head -5
    
    echo ""
    echo "=== Готово! ==="
    echo "🌐 Приложение доступно по адресу:"
    echo "   http://147.45.253.75"
    echo "   http://147.45.253.75:5173 (dev режим, если нужен)"
    echo ""
    echo "📊 API документация:"
    echo "   http://147.45.253.75/docs"
    echo ""
    echo "💚 Health Check:"
    echo "   http://147.45.253.75/health"
ENDSSH

echo ""
echo "✅ Развертывание завершено!"
echo ""
echo "🌐 Ваше приложение доступно по адресу:"
echo "   http://147.45.253.75"
echo ""
echo "📱 Для QR-кода используйте этот URL:"
echo "   http://147.45.253.75"

