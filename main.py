import requests
from bs4 import BeautifulSoup


def get_top_100_coins():
    url = "https://cryptobubbles.net"
    response = requests.get(url)
    response.raise_for_status()  # Убедимся, что запрос прошел успешно
    soup = BeautifulSoup(response.text, 'html.parser')

    coins = []
    for bubble in soup.select('.bubble'):
        coin = bubble.get('data-id')
        tradingview_link = bubble.select_one('.tradingview-link').get('href')
        coins.append((coin, tradingview_link))

    return coins


def format_coin_data(coins):
    formatted_coins = []
    for coin, link in coins:
        # Пример ссылки: "https://www.tradingview.com/symbols/BINANCE-ETHUSDT/"
        parts = link.split('/')
        if len(parts) > 4:
            formatted_coin = parts[-2]
            formatted_coins.append(formatted_coin)

    return formatted_coins


def main():
    coins = get_top_100_coins()
    formatted_coins = format_coin_data(coins)
    for coin in formatted_coins:
        print(coin)


if __name__ == "__main__":
    main()
