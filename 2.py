from bottle import route, run, request
import requests


@route('/')
def hello():
    response = "<html><body><h1>Hello World!</h1></body></html>"
    return response


@route('/currency')
def get_currency():
    # Базовий URL API НБУ
    nbu_api_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    # Отримання параметра запиту
    query = request.query.get('query', '').lower()

    # Логіка для сьогоднішнього або вчорашнього курсу
    if query == 'today':
        date = 'today'
    elif query == 'yesterday':
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        date = yesterday.strftime('%Y%m%d')  
    else:
        return "Unknown query. Supported queries are /currency?query=today or /currency?query=yesterday"

    # Виконання запиту до НБУ
    try:
        response = requests.get(f"{nbu_api_url}&date={date}")
        response.raise_for_status()
        data = response.json()

        # Перевірка, чи є дані
        if not data:
            return f"No data available for {query}"

        # Вибір першої валюти (наприклад, USD)
        usd_rate = next((item for item in data if item['cc'] == 'USD'), None)
        if not usd_rate:
            return "USD exchange rate not found"

        return f"Exchange rate for {query}: 1 USD = {usd_rate['rate']} UAH"
    except requests.RequestException as e:
        return f"Error fetching currency data: {e}"


if __name__ == '__main__':
    run(port=8000)
