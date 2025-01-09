import matplotlib.pyplot as plt
import requests
import json

# URL для запиту курсу валют
url = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20240916&end=20240920&valcode=usd&json"

try:
    # Виконання запиту до API
    response = requests.get(url)
    response.raise_for_status()  # Перевірка статусу відповіді

    # Завантаження JSON-відповіді
    data = response.json()

    # Перевірка, чи отримані дані
    if not data:
        print("No data received from the API.")
        exit()

    # Створення словника з датами та курсами
    exchange_rates = {item['exchangedate']: item['rate'] for item in data}

    # Сортування даних за датою
    sorted_dates = sorted(exchange_rates.keys(), key=lambda x: tuple(map(int, x.split('.'))))
    sorted_rates = [exchange_rates[date] for date in sorted_dates]

    # Візуалізація даних
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sorted_rates, marker='o', color='b', label='USD/UAH Rate')
    plt.title('Exchange Rate USD to UAH', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Exchange Rate (UAH)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()  # Автоматичне підлаштування компонентів графіка
    plt.show()

except requests.RequestException as e:
    print(f"Error fetching data: {e}")
except json.JSONDecodeError:
    print("Error decoding JSON response.")
