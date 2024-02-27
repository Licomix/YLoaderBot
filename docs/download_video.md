### Документация по utils/download_video.py

#### Функция `download_tiktok`

```python
async def download_tiktok(url, output_path="downloads", message=None, format="mp4"):
    """
    Загружает видео TikTok по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес TikTok видео.
        - output_path (str): Путь для сохранения загруженного видео (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки видео.
        - format (str): Формат сохраняемого контента. Доступные варианты MP3 и MP4 (по умолчанию: "MP4")

    Примечание:
        - Если указан параметр `message`, после загрузки видео отправляет его пользователю.
        - Видео сохраняется в формате MP4 в указанной директории.
    """
    url = requests.get(url)
    match = re.search(r'/video/(\d+)', url.url)
    if match:
        video_id = match.group(1)
    try:
        response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')
        filename = f"{output_path}/{video_id}.{format}"
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)

            if os.path.exists(filename) and message:

                if format == "mp3":
                    mp3_filename = f"{output_path}/{video_id}.mp3"
                    await convert_video_to_mp3(filename, mp3_filename)
                    await message.answer_voice(voice=types.InputFile(mp3_filename))
                    os.remove(mp3_filename)

                elif format == "mp4":
                    await message.answer_video(video=types.InputFile(filename))
                    os.remove(filename)
```
### Функция `convert_video_to_mp3`
```python
async def convert_video_to_mp3(video_path, output_path):
    """
    Конвертирует видео в MP3. Используется только для скачивания с TikTok.
    """
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='mp3')
    audio_clip.close()
    video_clip.close()
```
#### Функция `download_youtube`

```python
async def download_youtube(url, output_path="downloads", message=None, format="mp4"):
    """
    Загружает видео с YouTube по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес YouTube видео.
        - output_path (str): Путь для сохранения загруженного видео (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки видео.
        - format (str): Формат сохраняемого контента. Доступные варианты MP3 и MP4 (по умолчанию: "MP4")

    Примечание:
        - Если указан параметр `message`, после загрузки видео отправляет его пользователю.
        - Видео сохраняется в формате, указанном в метаданных YouTube видео.
    """
        # Определяем формат
    if format == "mp4":
        options = {
        'format': 'best[filesize_approx<50M]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')
                filename = ydl.prepare_filename(info_dict)
                ydl.download([url])
                if os.path.exists(filename) and message:
                    video = open(f'{filename}', 'rb')
                    await message.answer_video(caption=title, video=video)
                    os.remove(filename)
            except Exception as e:
                logging.error(f"Error downloading YouTube video: {str(e)}")
                logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")

    elif format == "mp3":
        try:
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
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')
                filename_ydlp = f'{ydl.prepare_filename(info_dict)[:-3]}mp3'
                filename_release = "downloads/" + remove_special_characters(f'{title}.mp3')

                ydl.download([url])
                thumbnail_filename = os.path.join(output_path, remove_special_characters(info_dict['title']))

                if os.path.exists(filename_ydlp) and message:
                    thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

                    # Сохраняем обложку
                    if thumbnail_path:
                        thumbnail_response = requests.get(thumbnail_path)

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
                os.rename(filename_ydlp, filename_release)
                await message.answer_audio(audio=types.InputFile(filename_release), thumb=types.InputFile(f"{thumbnail_filename}.jpg"))

                os.remove(filename_release)
                os.remove(f"{thumbnail_filename}.jpg")

        except yt_dlp.DownloadError as e:
            logging.error(f"Не удалось скачать видео: {str(e)}")
            await message.answer(f"Не удалось скачать музыку с видео: {str(e)}")
        except Exception as e:
            logging.error(f"Error downloading YouTube Audio: {str(e)}")
            logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
            await message.answer("Не удалось скачать музыку с видео по неизвестной ошибке.")
```

#### Общая информация

- Используется библиотека `yt_dlp` для работы с YouTube API.
- Для обработки URL TikTok видео используется регулярное выражение.
- Загруженные видео сохраняются в указанной директории, и, если указан параметр `message`, отправляются пользователю.
- В случае YouTube видео, выбирается наилучшее качество видео и аудио, при условии, что размер файла не превышает 50 МБ.

### Функция `remove_special_characters`

```python
def remove_special_characters(input_string):
    """
    Простая функция для удаление спецсимволов из строки.
    Параметры:
        - input_string (str): Строка, которую надо отредактировать.
    """
    # Удаление спецсимволов
    cleaned_string = re.sub(r'[\\/:*?"<>|]', '', input_string)
    return cleaned_string
```
