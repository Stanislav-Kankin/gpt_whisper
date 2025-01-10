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
            return f"Ваш баланс: {balance}"
        else:
            return f"Ошибка: {response.status_code}, {response.text}"
    except Exception as e:
        logger.error(f"Ошибка при проверке баланса: {e}")
        return f"Ошибка при проверке баланса: {e}"


if __name__ == "__main__":
    # Проверяем баланс и выводим результат
    result = check_balance()
    print(result)
