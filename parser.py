import os
import re
import logging
from email import message_from_string

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для извлечения ссылок и торговых пар из MHTML
def extract_trading_pairs_from_mhtml(mhtml_file):
    logging.info(f"Обрабатываем файл: {mhtml_file}")

    trading_pairs = []

    try:
        with open(mhtml_file, 'r', encoding='utf-8') as file:
            mhtml_content = file.read()

        logging.debug(f"Размер содержимого файла: {len(mhtml_content)} байт")

        # Парсим MHTML как email-сообщение
        msg = message_from_string(mhtml_content)

        # Проходим по частям MHTML-сообщения
        for part in msg.walk():
            content_type = part.get_content_type()

            logging.debug(f"Обрабатываем часть с типом: {content_type}")

            if content_type in ['text/html', 'text/plain']:
                # Получаем содержимое
                content = part.get_payload(decode=True).decode('utf-8', errors='ignore')

                logging.debug(f"Найдено содержимое длиной {len(content)} символов")

                # Объединяем строки с разрывами, убирая символы переноса
                content = content.replace('\n', '').replace('\r', '')

                # Ищем все ссылки, содержащие 'https://www.tradingview.com/chart/?symbol=' и '&amp;aff_id='
                links = re.findall(r'https://www\.tradingview\.com/chart/\?symbol=([A-Za-z0-9:]+)&amp;aff_id=', content)

                for link in links:
                    trading_pairs.append(link)

        logging.info(f"Найдено {len(trading_pairs)} торговых пар в файле {mhtml_file}.")
        return trading_pairs

    except Exception as e:
        logging.error(f"Ошибка при обработке файла {mhtml_file}: {e}")
        return []

# Функция для обработки всех .mhtml файлов в папке
def process_mhtml_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Создаём выходную папку, если её нет

    # Получаем список всех mhtml файлов в папке
    mhtml_files = [f for f in os.listdir(input_folder) if f.endswith('.mhtml')]

    for mhtml_file in mhtml_files:
        mhtml_file_path = os.path.join(input_folder, mhtml_file)

        # Извлекаем торговые пары из файла
        trading_pairs = extract_trading_pairs_from_mhtml(mhtml_file_path)

        if trading_pairs:
            # Сохраняем результат в текстовый файл с таким же именем, но с расширением .txt
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(mhtml_file)[0]}.txt")

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for pair in trading_pairs:
                    output_file.write(pair + '\n')

            logging.info(f"Торговые пары из файла {mhtml_file} сохранены в {output_file_path}.")
        else:
            logging.warning(f"Не удалось найти торговые пары в файле {mhtml_file}.")

# Пример использования
input_folder = 'out'  # Папка с входными .mhtml файлами
output_folder = 'out'  # Папка для сохранения текстовых файлов с торговыми парами

process_mhtml_files(input_folder, output_folder)
