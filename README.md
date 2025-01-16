### Требования
# Для запуска проекта вам понадобятся:

Python 3.9 или выше

Docker и Docker Compose (опционально, для запуска через контейнеры)

API-ключ от OpenAI (или ProxyAPI)

Токен Telegram-бота

## Запуск локально

# 1. Клонируйте репозиторий

```git clone https://github.com/your_username/your_repository.git```

Перейдите в папку с проектом:

```cd your_repository```

# 2. Установите зависимости

Создайте виртуальное окружение и установите зависимости:
`python -m venv env`

Активация на Linux:
`source env/bin/activate`

Активация на Windows:
`env\Scripts\activate`

Усталоновите зависимости:
`pip install -r requirements.txt`

# 3. Настройте переменные окружения
Создайте файл .env в корне проекта и добавьте туда следующие переменные:

Токен Вашего бота:
`BOT_TOKEN=your_telegram_bot_token`

API ключ для доступа к OpenAI:
`PROXY_API_KEY=your_proxy_api_key`

# 4. Запустите бота

`python bot.py`

Бот работает!

## Запуск на удалённом сервере
1. Подключитесь к серверу

Подключитесь к вашему серверу по SSH:
`ssh user@your_server_ip`

# 2. Установите Docker и Docker Compose
Если Docker и Docker Compose ещё не установлены, выполните:

`sudo apt update`
`sudo apt install docker.io docker-compose`
`sudo systemctl enable docker`
`sudo systemctl start docker`

# 3. Клонируйте репозиторий

Клонируйте репозиторий на сервер:
`git clone https://github.com/your_username/your_repository.git`

Перейдите в папку с проектом:
`cd your_repository`

# 4. Настройте переменные окружения
Создайте файл .env в корне проекта и добавьте туда следующие переменные:

Токен Вашего бота:
`BOT_TOKEN=your_telegram_bot_token`

API ключ для доступа к OpenAI:
`PROXY_API_KEY=your_proxy_api_key`

# 5. Запустите приложение с помощью Docker Compose

`docker-compose up -d`

Использование Docker:

Сборка Docker-образа
Чтобы собрать Docker-образ вручную, выполните:

bash
Copy
docker build -t my-telegram-bot .
Запуск контейнера
Запустите контейнер с помощью Docker:

bash
Copy
docker run -d --name my-bot-container my-telegram-bot
Остановка и удаление контейнера
Чтобы остановить и удалить контейнер, выполните:

bash
Copy
docker stop my-bot-container
docker rm my-bot-container
Обновление приложения
Локально
Внесите изменения в код.

Закоммитьте и отправьте изменения в репозиторий:

bash
Copy
git add .
git commit -m "Ваше сообщение о изменениях"
git push origin main
На сервере
Подключитесь к серверу по SSH:

bash
Copy
ssh user@your_server_ip
Перейдите в директорию с проектом:

bash
Copy
cd /path/to/your_repository
Получите последние изменения из репозитория:

bash
Copy
git pull origin main
Пересоберите и перезапустите контейнер:

bash
Copy
docker-compose up -d --build
Переменные окружения
Переменная	Описание
BOT_TOKEN	Токен вашего Telegram-бота.
PROXY_API_KEY	API-ключ от ProxyAPI или OpenAI.
