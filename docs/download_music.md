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
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'audio')
            filename = ydl.prepare_filename(info_dict)

        if os.path.exists(filename) and message:
            await message.answer_audio(caption=title, audio=types.InputFile(filename))
            os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")
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
    result = spotify.track(url)
    performers = ", ".join([artist['name'] for artist in result['artists']])
    music = result['name']

    videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
    videoresult = videosSearch.result()["result"][0]["link"]

    filename = f'{output_path}/{performers}_{music}.mp3'
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': filename,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([videoresult])

        if os.path.exists(filename) and message:
            await message.answer_audio(audio=types.InputFile(filename))
            os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")
```

#### Общая информация

- Для загрузки аудио с SoundCloud используется библиотека `yt_dlp`.
- Для загрузки аудио с Spotify используется библиотеки `spotipy` и `youtubesearchpython`.
- Для загрузки аудио с Apple Music используется библиотеки `requests` и `youtubesearchpython`.
- Загруженные аудио сохраняются в указанной директории, и, если указан параметр `message`, отправляются пользователю.
- В обеих функциях аудио сохраняется в формате MP3.
