# FROM python:3.11-slim
#
# RUN apt-get update && apt-get install -y \
#     libnss3 \
#     libatk-bridge2.0-0 \
#     libatk1.0-0 \
#     libcups2 \
#     libx11-xcb1 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxfixes3 \
#     libxi6 \
#     libxrandr2 \
#     libxrender1 \
#     libpangocairo-1.0-0 \
#     libpango-1.0-0 \
#     libasound2 \
#     fonts-liberation \
#     && rm -rf /var/lib/apt/lists/*
#
# ENV CHROME_BIN=/usr/bin/chromium
# ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
#
# WORKDIR /AR_scraper
#
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# COPY . /AR_scraper
#
# CMD ["python", "main.py"]

# Используем легкий Python образ
FROM python:3.11-slim

# Устанавливаем все зависимости для Chromium + шрифты
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libasound2 \
    fonts-liberation \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Пути к бинарникам Chrome и драйвера
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Рабочая директория
WORKDIR /AR_scraper

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /AR_scraper

# Команда запуска
CMD ["python", "main.py"]