import re
import logging
from email import message_from_string

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для извлечения ссылок и торговых пар из MHTML
def extract_trading_pairs_from_mhtml(mhtml_file):
    # Логируем начало обработки файла
    logging.info(f"Начало обработки файла: {mhtml_file}")

    try:
        with open(mhtml_file, 'r', encoding='utf-8') as file:
            mhtml_content = file.read()

        logging.debug(f"Размер содержимого файла: {len(mhtml_content)} байт")

        # Парсим MHTML как email-сообщение
        msg = message_from_string(mhtml_content)

        trading_pairs = []

        # Проходим по частям MHTML-сообщения
        for part in msg.walk():
            content_type = part.get_content_type()

            # Логируем тип содержимого каждой части
            logging.debug(f"Обрабатываем часть с типом: {content_type}")

            # Если это текстовый контент (html или plain)
            if content_type in ['text/html', 'text/plain']:
                # Получаем содержимое
                content = part.get_payload(decode=True).decode('utf-8', errors='ignore')

                logging.debug(f"Найдено содержимое длиной {len(content)} символов")

                # Объединяем строки с разрывами, убирая символы переноса
                content = content.replace('\n', '').replace('\r', '')

                # Логируем первые 100 символов объединенного контента для проверки
                logging.debug(f"Первоначальные 100 символов содержимого: {content[:100]}")

                # Ищем все ссылки, содержащие 'https://www.tradingview.com/chart/?symbol=' и '&amp;aff_id='
                links = re.findall(r'https://www\.tradingview\.com/chart/\?symbol=([A-Za-z0-9:]+)&amp;aff_id=', content)

                # Выводим в консоль каждую найденную ссылку
                for link in links:
                    print(link)
                    trading_pairs.append(link)

        # Логируем завершение обработки
        logging.info(f"Обработка завершена. Найдено {len(trading_pairs)} торговых пар.")
        return trading_pairs

    except Exception as e:
        logging.error(f"Ошибка при обработке файла: {e}")
        return []

# Пример использования
mhtml_file = 'example.mhtml'  # Замените на путь к вашему файлу
trading_pairs = extract_trading_pairs_from_mhtml(mhtml_file)
print(trading_pairs)
