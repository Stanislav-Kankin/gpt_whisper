# Название проекта
GPT и Whisper Telegram Bot

## Описание
Этот проект представляет собой Telegram-бота, который использует GPT для обработки текста и Whisper для обработки аудио. Бот предназначен для внутреннего использования в компании и упрощает взаимодействие с AI-моделями через Telegram.

## Требования
Для запуска проекта вам понадобятся:
- Python 3.9 или выше.
- Docker и Docker Compose (опционально, для запуска через контейнеры).
- API-ключ от OpenAI (или ProxyAPI).
- Токен Telegram-бота.

## Установка и запуск
### Локальный запуск
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your_username/your_repository.git

2. Перейдите в папку с проектом:
    ```bash
    cd your_repository

3. Установите зависимости:
    ```bash
    python -m venv env
    source env/bin/activate  # Linux
    env\Scripts\activate     # Windows
    pip install -r requirements.txt

4. Настройте переменные окружения:

    Создайте файл .env в корне проекта и добавьте туда:

    ```bash
    BOT_TOKEN=your_telegram_bot_token
    PROXY_API_KEY=your_proxy_api_key

5. Запустите бота:

    ```bash
    python bot.py

### Запуск на удалённом сервере
1. Подключитесь к серверу по SSH:
    ```bash
    ssh user@your_server_ip

2. Установите Docker и Docker Compose (если не установлены):
    ```bash
    sudo apt update
    sudo apt install docker.io docker-compose
    sudo systemctl enable docker
    sudo systemctl start docker

3. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your_username/your_repository.git
    cd your_repository

4. Настройте переменные окружения (аналогично локальному запуску).

5. Запустите приложение с помощью Docker Compose:
    ```bash
    docker-compose up -d

### Использование Docker
1. Сборка Docker-образа:
    ```bash
    docker build -t my-telegram-bot .

2. Запуск контейнера:
    ```bash
    docker run -d --name my-bot-container my-telegram-bot

3. Остановка и удаление контейнера:
    ```bash
    docker stop my-bot-container
    docker rm my-bot-container


### Обновление приложения
## Локально:
1. Внесите изменения в код.
2. Закоммитьте и отправьте изменения:
    ```bash
    git add .
    git commit -m "Ваше сообщение о изменениях"
    git push origin main

## На сервере:
1. Подключитесь к серверу по SSH.
2. Перейдите в директорию с проектом:
    ```bash
    cd /path/to/your_repository
3. Получите последние изменения:
    ```bash
    git pull origin main
4. Пересоберите и перезапустите контейнер:
    ```bash
    docker-compose up -d --build
### Переменные окружения

[BOT_TOKEN] -`Токен вашего Telegram-бота.`
[PROXY_API_KEY] -`API-ключ от ProxyAPI или OpenAI.`
