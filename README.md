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