import requests
from config import config
from utils.logging import logger


def get_balance() -> float:
    """
    Получает текущий баланс аккаунта на ProxyAPI.
    Возвращает баланс в виде числа или None в случае ошибки.
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
            return float(balance)  # Преобразуем баланс в число
        else:
            logger.error(
                f"Ошибка при получении баланса: {response.status_code}, {response.text}"
                )
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении баланса: {e}")
        return None


def calculate_cost(before_balance: float, after_balance: float) -> float:
    """
    Рассчитывает стоимость операции на основе изменения баланса.
    Возвращает стоимость в рублях.
    """
    if before_balance is None or after_balance is None:
        logger.error("Не удалось получить баланс для расчета стоимости.")
        return 0.0

    cost = before_balance - after_balance
    return round(cost, 4)  # Округляем до 4 знаков после запятой
