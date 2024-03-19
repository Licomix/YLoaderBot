import logging
import yt_dlp
import os
import re
from aiogram.types import FSInputFile
import requests
from PIL import Image
from io import BytesIO
import re

async def download_tiktok(url, output_path="downloads", message=None, format="mp4"):
    if format == "mp4":
        try:
            # Устанаваливаем настройки для YT_dlp
            options = {
            'format': 'mp4',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                # Подготавливаем информацию про видео
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')
                filename = ydl.prepare_filename(info_dict)
                # Скачиваем
                ydl.download([url])
                # Если скачивание прошло успешно (файл существует), то отправляем полученное видео пользователю
                if os.path.exists(filename) and message:
                    # video = open(f'{filename}', 'rb')
                    await message.answer_video(caption=title, video=FSInputFile(filename))
                    os.remove(filename)
        # Хандлер ошибок
        except yt_dlp.DownloadError as e:
            logging.error(f"Не удалось скачать видео: {str(e)}")
            await message.answer(f"Простите. Мне не удалось скачать видео: {str(e)}")
        except Exception as e:
            logging.error(f"Error downloading Tiktok video: {str(e)}")
            logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
            await message.answer("Простите. Мне не удалось скачать это видео по неизвестной ошибке.")

    elif format == "mp3":
        try:
            # Устанаваливаем настройки для YT_dlp
            options = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'restrictfilenames': True,
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                # Подготавливаем информацию про видео
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')

                # Подготавливаем названия файлов для избежания ошибок из-за спец. символов
                filename_ydlp = f'{ydl.prepare_filename(info_dict)[:-3]}mp3'
                filename_release = "downloads/" + remove_special_characters(f'{title}.mp3')

                # Скачиваем
                ydl.download([url])

                # Проверяем на успешое скачивание файла
                if os.path.exists(filename_ydlp) and message:

                    # Переименовываем файл для избежания ошибок и отправляем пользователю
                    os.rename(filename_ydlp, filename_release)
                    await message.answer_audio(audio=FSInputFile(filename_release))

                    os.remove(filename_release)

        # Хандлер ошибок
        except yt_dlp.DownloadError as e:
            logging.error(f"Не удалось скачать видео: {str(e)}")
            await message.answer(f"Простите. Мне не удалось скачать музыку с видео: {str(e)}")
        except Exception as e:
            logging.error(f"Error downloading YouTube Audio: {str(e)}")
            logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
            await message.answer("Простите. Мне не удалось скачать музыку с видео по неизвестной ошибке.")

async def download_youtube(url, output_path="downloads", message=None, format="mp4"):
    # Определяем формат
    if format == "mp4":
        try:
            # Устанаваливаем настройки для YT_dlp
            options = {
            'format': 'mp4[filesize_approx<50M]',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                # Подготавливаем информацию про видео
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')
                filename = ydl.prepare_filename(info_dict)
                # Скачиваем
                ydl.download([url])
                # Если скачивание прошло успешно (файл существует), то отправляем полученное видео пользователю
                if os.path.exists(filename) and message:
                    await message.answer_video(caption=title, video=FSInputFile(filename))
                    os.remove(filename)
        # Хандлер ошибок
        except yt_dlp.DownloadError as e:
            logging.error(f"Не удалось скачать видео: {str(e)}")
            await message.answer(f"Простите. Мне не удалось скачать видео: {str(e)}")
        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
            await message.answer("Простите. Мне не удалось скачать это видео по неизвестной ошибке.")

    elif format == "mp3":
        try:
            # Устанаваливаем настройки для YT_dlp
            options = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'restrictfilenames': True,
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                # Подготавливаем информацию про видео
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')

                # Подготавливаем названия файлов для избежания ошибок из-за спец. символов
                filename_ydlp = f'{ydl.prepare_filename(info_dict)[:-3]}mp3'
                filename_release = "downloads/" + remove_special_characters(f'{title}.mp3')

                # Скачиваем
                ydl.download([url])
                thumbnail_filename = os.path.join(output_path, remove_special_characters(info_dict['title']))

                # Проверяем на успешое скачивание файла
                if os.path.exists(filename_ydlp) and message:
                    thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

                    # Сохраняем обложку
                    if thumbnail_path:
                        thumbnail_response = requests.get(thumbnail_path)

                        # Редактируем обложку. Вырезаем из середины квадрат для лучшего отображение
                        with BytesIO(thumbnail_response.content) as thumbnail_file:
                            original_image = Image.open(thumbnail_file)
                            width, height = original_image.size
                            new_size = min(width, height)
                            left = (width - new_size) / 2
                            top = (height - new_size) / 2
                            right = (width + new_size) / 2
                            bottom = (height + new_size) / 2
                            cropped_image = original_image.crop((left, top, right, bottom))

                            cropped_image.save(f"{thumbnail_filename}.jpg")

                # Переименовываем файл для избежания ошибок и отправляем пользователю
                os.rename(filename_ydlp, filename_release)
                await message.answer_audio(audio=FSInputFile(filename_release), thumb=FSInputFile(f"{thumbnail_filename}.jpg"))

                os.remove(filename_release)
                os.remove(f"{thumbnail_filename}.jpg")

        # Хандлер ошибок
        except yt_dlp.DownloadError as e:
            logging.error(f"Не удалось скачать видео: {str(e)}")
            await message.answer(f"Простите. Мне не удалось скачать музыку с видео: {str(e)}")
        except Exception as e:
            logging.error(f"Error downloading YouTube Audio: {str(e)}")
            logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
            await message.answer("Простите. Мне не удалось скачать музыку с видео по неизвестной ошибке.")

def remove_special_characters(input_string):
    # Удаление спецсимволов
    cleaned_string = re.sub(r'[\\/:*?"<>|]', '', input_string)
    return cleaned_string
