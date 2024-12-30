from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_top_100_coins():
    # Инициализируем веб-драйвер
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://cryptobubbles.net")

    # Дожидаемся загрузки элементов
    driver.implicitly_wait(10)

    coins = []
    bubbles = driver.find_elements(By.CSS_SELECTOR, '.bubble')
    for bubble in bubbles:
        coin = bubble.get_attribute('data-id')
        tradingview_link = bubble.get_attribute('data-symbol-link')
        print(f"Found coin: {coin}, TradingView link: {tradingview_link}")  # Отладочный вывод
        if coin and tradingview_link:
            coins.append((coin, tradingview_link))

    driver.quit()
    return coins

def format_coin_data(coins):
    formatted_coins = []
    for coin, link in coins:
        # Пример ссылки: "https://www.tradingview.com/symbols/BINANCE-ETHUSDT/"
        parts = link.split('/')
        if len(parts) > 4:
            formatted_coin = parts[-2].replace('-', ':')
            formatted_coins.append(formatted_coin)
            print(f"Formatted coin: {formatted_coin}")  # Отладочный вывод

    return formatted_coins

def main():
    coins = get_top_100_coins()
    print(f"Coins: {coins}")  # Отладочный вывод
    formatted_coins = format_coin_data(coins)
    for coin in formatted_coins:
        print(coin)

if __name__ == "__main__":
    main()
