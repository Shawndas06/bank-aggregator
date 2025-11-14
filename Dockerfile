# Монолитный Dockerfile для деплоя Backend + Frontend вместе
# Подходит для Render.com, Fly.io и других хостингов с Docker поддержкой

# ==================== Stage 1: Frontend Build ====================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Устанавливаем pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Копируем package.json и устанавливаем зависимости
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Копируем исходники и собираем
COPY frontend/ ./
RUN pnpm run build

# ==================== Stage 2: Backend Build ====================
FROM python:3.11-slim AS backend-builder

WORKDIR /app/backend

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем Python зависимости
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend код
COPY backend/ ./

# ==================== Stage 3: Final Image ====================
FROM python:3.11-slim

WORKDIR /app

# Устанавливаем nginx и системные зависимости
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/nginx/sites-enabled/default

# Копируем backend из builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY --from=backend-builder /app/backend /app/backend

# Копируем frontend из builder
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Копируем конфигурации
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Создаём директории
RUN mkdir -p /app/logs /var/log/supervisor

# Expose порт
EXPOSE 80

# Запускаем supervisor для управления процессами
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

