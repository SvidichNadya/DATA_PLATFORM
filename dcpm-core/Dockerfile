# Базовый образ Python 3.11 slim
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Устанавливаем Poetry (только один раз)
RUN pip install --no-cache-dir "poetry>=2.3.2"

# Настраиваем Poetry: использовать системный python, без виртуальных окружений
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY pyproject.toml /app/

# Создаем lock-файл если его нет
RUN if [ ! -f poetry.lock ]; then poetry lock; fi

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем весь код
COPY . /app/

# FastAPI порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]