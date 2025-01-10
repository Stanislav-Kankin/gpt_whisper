import requests
from config import config
from utils.logging import logger


def check_balance() -> str:
    """
    Проверяет баланс аккаунта на ProxyAPI.
    Возвращает строку с балансом или сообщение об ошибке.
    """
    try:
        # URL для проверки баланса
        url = "https://api.proxyapi.ru/proxyapi/balance"

        # Заголовок с ключом API
        headers = {
            "Authorization": f"Bearer {config.PROXY_API_KEY}"
        }

        # Отправляем GET-запрос
        response = requests.get(url, headers=headers)

        # Проверяем ответ
        if response.status_code == 200:
            balance = response.json().get("balance")
            return f"Ваш текущий баланс: {balance}"
        else:
            return f"Ошибка при проверке баланса: {response.status_code}, {response.text}"
    except Exception as e:
        logger.error(f"Ошибка при проверке баланса: {e}")
        return f"Ошибка при проверке баланса: {e}"


def estimate_cost(text: str, model: str = "gpt-3.5-turbo") -> float:
    """
    Оценивает стоимость операции в токенах.
    Возвращает стоимость в рублях.
    """
    try:
        # Примерная стоимость токенов (в рублях за 1000 токенов)
        cost_per_thousand_tokens = {
            "whisper-1": 0.006,  # Примерная стоимость транскрибации
            "gpt-3.5-turbo": 0.002  # Примерная стоимость анализа
        }

        # Оцениваем количество токенов (примерно 1 токен = 4 символа)
        num_tokens = len(text) / 4

        # Рассчитываем стоимость
        cost = (num_tokens / 1000) * cost_per_thousand_tokens.get(model, 0.002)
        return round(cost, 4)  # Округляем до 4 знаков после запятой
    except Exception as e:
        logger.error(f"Ошибка при оценке стоимости: {e}")
        return 0.0
