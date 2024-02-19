import os
import requests
from PIL import Image  # библиотека для работы с изображениями, Вы можете использовать другую
from time import perf_counter


def download_and_resize_images(image_urls, output_directory, max_width, max_height):
    # Создаем папки для оригинальных картинок и уменьшенных версий
    original_dir = os.path.join(output_directory, "original")
    resized_dir = os.path.join(output_directory, "resized")
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(resized_dir, exist_ok=True)

    for url in image_urls:
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

            # # Открываем исходную картинку с помощью PIL
            # image = Image.open(original_path)
            #
            # # Масштабируем картинку до желаемых размеров
            # image.thumbnail((max_width, max_height))
            #
            # # Создаем новое имя для уменьшенной копии
            # resized_filename = f"resized_{filename}"
            #
            # # Сохраняем уменьшенную копию картинки в папке "resized"
            # resized_path = os.path.join(resized_dir, resized_filename)
            # image.save(resized_path)
            # print(f"Успешно создано уменьшенное изображение: {resized_filename}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обработке URL-адреса: {url}")
            print(f"Ошибка: {e}")
        except IOError as e:
            print(f"Ошибка при обработке файла: {filename}")
            print(f"Ошибка: {e}")


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

start_time = perf_counter()
download_and_resize_images(urls, output_directory, max_width, max_height)
print(f"ALL DONE, {perf_counter() - start_time}")