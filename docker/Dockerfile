# Базовый образ: Python 3.12 в облегчённой сборке
FROM python:3.12-slim

# Логи без буферизации (появляются сразу), без .pyc файлов
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Рабочая папка внутри контейнера
WORKDIR /app

# Сначала зависимости: этот слой кэшируется, пока requirements.txt не менялся
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем код и SQL-скрипты
COPY src ./src
COPY sql ./sql

# Всегда запускаю CLI, формат передаётся аргументом (см. docker-compose.yml)
ENTRYPOINT ["python", "-m", "src.cli"]
CMD ["--format", "json"]