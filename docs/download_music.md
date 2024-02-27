### Документация по utils/download_music.py

#### Функция `download_soundcloud`

```python
async def download_soundcloud(url, output_path="downloads", message=None):
    """
    Загружает аудио с SoundCloud по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес SoundCloud трека.
        - output_path (str): Путь для сохранения загруженного аудио (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки аудио.

    Примечание:
        - Если указан параметр `message`, после загрузки аудио отправляет его пользователю.
        - Аудио сохраняется в формате MP3 в указанной директории.
    """
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'writethumbnail': True,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])

        filename = os.path.join(output_path, f"{info_dict['title']}.mp3")
        thumbnail_filename = os.path.join(output_path, f"{info_dict['title']}")

        if os.path.exists(filename) and message:
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

        await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(f"{thumbnail_filename}.jpg"))

        os.remove(filename)
        os.remove(f"{thumbnail_filename}.jpg")
    except Exception as e:
        logging.error(f"Error downloading YouTube Audio: {str(e)}")
        logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
        await message.answer(text="Простите. Мне не удалось скачать музыку с SoundCloud.")
```

#### Функция `download_spotify`

```python
async def download_spotify(url, output_path="downloads", message=None):
    """
    Загружает аудио с Spotify по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес Spotify трека.
        - output_path (str): Путь для сохранения загруженного аудио (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки аудио.

    Примечание:
        - Если указан параметр `message`, после загрузки аудио отправляет его пользователю.
        - Для поиска трека на YouTube используется библиотека youtubesearchpython.
        - Аудио сохраняется в формате MP3 в указанной директории.
    """
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'writethumbnail': True,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])

        filename = os.path.join(output_path, f"{info_dict['title']}.mp3")
        thumbnail_filename = os.path.join(output_path, f"{info_dict['title']}")

        if os.path.exists(filename) and message:
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

        await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(f"{thumbnail_filename}.jpg"))

        os.remove(filename)
        os.remove(f"{thumbnail_filename}.jpg")
    except Exception as e:
        logging.error(f"Error downloading YouTube Audio: {str(e)}")
        logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
        await message.answer(text="Простите. Мне не удалось скачать музыку с SoundCloud.")

async def download_spotify(url, output_path="downloads", message=None):
    result = spotify.track(url)
    performers = ", ".join([artist['name'] for artist in result['artists']])
    music = result['name']

    videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
    videoresult = videosSearch.result()["result"][0]["link"]

    filename = f'{output_path}/{performers} - {music}'
    thumbnail_filename = f'{output_path}/{performers}_{music}'

    options = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(videoresult, download=False)
            ydl.download([videoresult])
        filename = f'{filename}.mp3'

        if os.path.exists(filename) and message:
            thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

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

        await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(f"{thumbnail_filename}.jpg"))

        os.remove(filename)
        os.remove(f"{thumbnail_filename}.jpg")
    except Exception as e:
        logging.error(f"Error downloading YouTube Audio: {str(e)}")
        logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
        await message.answer(text="Простите. Мне не удалось скачать музыку с Spotify.")
```
#### Функция `download_apple_music`

```python
async def download_apple_music(url, output_path="downloads", message=None):
    """
    Загружает аудио с Apple Music по указанному URL-адресу.

    Параметры:
        - url (str): URL-адрес Spotify трека.
        - output_path (str): Путь для сохранения загруженного аудио (по умолчанию: "downloads").
        - message (obj): Объект сообщения для отправки аудио.

    Примечание:
        - Если указан параметр `message`, после загрузки аудио отправляет его пользователю.
        - Для поиска трека на YouTube используется библиотека youtubesearchpython.
        - Аудио сохраняется в формате MP3 в указанной директории.
    """
    song_id = url.split('i=')[-1]
    api_url = f'https://itunes.apple.com/lookup?id={song_id}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        track_info = data.get('results', [])[0]

        if track_info:
            music = track_info.get('trackName')
            performers = track_info.get('artistName')

            videos_search = VideosSearch(f'{performers} - {music}', limit=1)
            video_result = videos_search.result()["result"][0]["link"]

            filename = f'{output_path}/{performers} - {music}'
            thumbnail_filename = f'{output_path}/{performers}_{music}'

            options = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(video_result, download=False)
                ydl.download([video_result])
            filename = f'{filename}.mp3'

            if os.path.exists(filename) and message:
                thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

                if thumbnail_path:
                    thumbnail_response = requests.get(thumbnail_path)
                    with open(thumbnail_filename, 'wb') as thumbnail_file:
                        thumbnail_file.write(thumbnail_response.content)

                await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(thumbnail_filename))

                os.remove(filename)
                os.remove(thumbnail_filename)

        else:
            await message.send('Информация о трэке не найдена')

    except Exception as e:
        logging.error(f"Error downloading YouTube Audio: {str(e)}")
        logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
        await message.answer(text="Простите. Мне не удалось скачать музыку с Apple Music")
```
#### Общая информация

- Для загрузки аудио с SoundCloud используется библиотека `yt_dlp`.
- Для загрузки аудио с Spotify используется библиотеки `spotipy` и `youtubesearchpython`.
- Для загрузки аудио с Apple Music используется библиотеки `requests` и `youtubesearchpython`.
- Загруженные аудио сохраняются в указанной директории, и, если указан параметр `message`, отправляются пользователю.
- В обеих функциях аудио сохраняется в формате MP3.
