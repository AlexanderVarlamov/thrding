import concurrent.futures
import logging
import multiprocessing
import os
import threading
from datetime import datetime
from time import perf_counter

import requests
from PIL import Image  # библиотека для работы с изображениями, Вы можете использовать другую

urls = [
    'https://apod.nasa.gov/apod/image/2310/IC63_GruntzBax.jpg',
    'https://apod.nasa.gov/apod/image/2310/2P_Encke_2023_08_24JuneLake_California_USA_DEBartlett.jpg',
    'https://apod.nasa.gov/apod/image/2310/20231023_orionids_in_taurus_1440b.jpg',
    'https://apod.nasa.gov/apod/image/2310/Arp87_HubblePathak_2512.jpg',
    'https://apod.nasa.gov/apod/image/2310/C2023H2LemmonGalaxies.jpg',
    'https://apod.nasa.gov/apod/image/2310/WesternVeil_Wu_2974.jpg',
    'https://apod.nasa.gov/apod/image/2310/M33_Triangulum.jpg',
    'https://apod.nasa.gov/apod/image/2310/MuCephei_apod.jpg',
    'https://apod.nasa.gov/apod/image/2310/Hourglass_HubblePathak_1080.jpg',
    'https://apod.nasa.gov/apod/image/2310/HiResSprites_Escurat_3000.jpg',
    'https://apod.nasa.gov/apod/image/2309/M8-Mos-SL10-DCPrgb-st-154-cC-cr.jpg',
    'https://apod.nasa.gov/apod/image/2309/BlueHorse_Grelin_93.jpg',
    'https://apod.nasa.gov/apod/image/2309/Arp142_HubbleChakrabarti_2627.jpg',
    'https://apod.nasa.gov/apod/image/2309/HH211_webb_3846.jpg',
    'https://apod.nasa.gov/apod/image/2309/LRGBHa23_n7331r.jpg',
    'https://apod.nasa.gov/apod/image/2309/PolarRing_Askap_960.jpg',
    'https://apod.nasa.gov/apod/image/2309/STSCI-HST-abell370_1797x2000.jpg'
]

output_directory = "./nasa_foto"
max_width = 600
max_height = 400

original_dir = os.path.join(output_directory, "original")
resized_dir = os.path.join(output_directory, "resized")
os.makedirs(original_dir, exist_ok=True)
os.makedirs(resized_dir, exist_ok=True)

info_logger = multiprocessing.get_logger()
info_logger.setLevel(logging.INFO)
fh = logging.FileHandler('test_log.txt', encoding='utf-8')
formatter = logging.Formatter(fmt="{processName}, {asctime}, {message}", style='{')
fh.setFormatter(formatter)
info_logger.addHandler(fh)

def download_image(url: str, queue, info_queue):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Получаем имя файла из URL-адреса
        filename = url.split('/')[-1]

        # Сохраняем исходную картинку в папку "original"
        original_path = os.path.join(original_dir, filename)
        with open(original_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=4096):
                file.write(chunk)
        queue.put(original_path)

    except requests.exceptions.RequestException as e:
        info_queue.put(f"ERROR: {datetime.now()} Ошибка при обработке URL-адреса: {url}")
        info_queue.put(f"ERROR: {datetime.now()} Ошибка: {e}")
    except IOError as e:
        info_queue.put(f"ERROR: {datetime.now()} Ошибка при обработке файла: {filename}")
        info_queue.put(f"ERROR: {datetime.now()} Ошибка: {e}")


def resize_images(queue: multiprocessing.Queue, info_queue):
    while True:
        try:
            original_path = queue.get()
            if original_path is None:
                queue.put(None)
                break
            else:
                info_queue.put(f'INFO {datetime.now()} Получен файл {original_path}. Открываем файл')
                info_logger.info(f'INFO {datetime.now()} Получен файл {original_path}. Открываем файл')
                image = Image.open(original_path)
                info_queue.put(f'INFO {datetime.now()} Файл {original_path} открыт успешно')
                info_logger.info(f'INFO {datetime.now()} Файл {original_path} открыт успешно')
                # Масштабируем картинку до желаемых размеров
                image.thumbnail((max_width, max_height))
                filename = original_path.split(os.sep)[-1]
                info_queue.put(f'INFO {datetime.now()} Файл {original_path} масштабирован успешно')
                info_logger.info(f'INFO {datetime.now()} Файл {original_path} масштабирован успешно')

                # Создаем новое имя для уменьшенной копии
                resized_filename = f"resized_{filename}"
                # Сохраняем уменьшенную копию картинки в папке "resized"
                resized_path = os.path.join(resized_dir, resized_filename)
                image.save(resized_path)
                info_queue.put(f"INFO {datetime.now()} Успешно создано уменьшенное изображение: {resized_filename}")
                info_logger.info(f"INFO {datetime.now()} Успешно создано уменьшенное изображение: {resized_filename}")
        except Exception as e:
            info_queue.put(f"ERROR {datetime.now()} {e}")


def log_to_file(logging_queue: multiprocessing.Queue, error_queue: multiprocessing.Queue = None) -> None:
    """
    Функция логирования в два файла
    :param logging_queue: очередь сообщений
    :param error_queue: отдельная очередь для сообщений была бы лучше, не реализовано
    :return: Nothing
    """
    while True:
        try:
            line: str = logging_queue.get()
            if line is None:
                break
            else:
                if line.startswith('ERROR'):
                    print(line)
                    with open('log_error.txt', 'a', encoding='utf-8') as file:
                        file.write(line + '\n')
                if line.startswith('END'):
                    print(line)
                with open('log_info.txt', 'a', encoding='utf-8') as file:
                    file.write(line + '\n')
        except TimeoutError as tme:
            # error_queue.put(f"Очередь сообщений пуста уже {timeout} секунд")
            with open('log_error.txt', 'a', encoding='utf-8') as file:
                file.write(str(tme) + '\n')
            break
        except Exception as e:
            # error_queue.put(f"Ошибка {e}. Продолжаю чтение лога")
            with open('log_error.txt', 'a', encoding='utf-8') as file:
                file.write(str(e) + '\n')
            continue


def main():
    start_time = perf_counter()
    files_queue = multiprocessing.Queue()  # очередь для путей-файлов
    info_queue = multiprocessing.Queue()  # очередь для сообщений
    info_queue.put(f"\n{datetime.now()}\n".center(100, '-'))
    # создаём поток-логгер
    logger = threading.Thread(target=log_to_file, args=(info_queue,), daemon=True)
    logger.start()
    # качаем файлы потоками
    with concurrent.futures.ThreadPoolExecutor() as executor:
        files = []
        for url in urls:
            files.append(executor.submit(download_image, url, files_queue, info_queue))
        # а обрабатываем процессами
        processes = [
            multiprocessing.Process(target=resize_images,
                                    args=(files_queue, info_queue)) for _ in range(multiprocessing.cpu_count())]
        for proc in processes:
            proc.start()
        concurrent.futures.wait(files)
        info_queue.put(f'END {datetime.now()} All files are downloaded')
        files_queue.put(None)
        for proc in processes:
            proc.join()

    info_queue.put(f"END {datetime.now()} ALL DONE, {perf_counter() - start_time}\n")
    info_queue.put(None)
    # завершаем поток логгера
    logger.join()


if __name__ == '__main__':
    main()
