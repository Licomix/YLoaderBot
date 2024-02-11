import logging
import yt_dlp
import os
import re
from aiogram import types
import requests
from moviepy.editor import VideoFileClip

async def download_tiktok(url, output_path="downloads", message=None, format="mp4"):
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

        else:
            logging.error(f"Error downloading TikTok video. HTTP status code: {response.status_code}")
    except FileNotFoundError:
        logging.error(f"FileNotFoundError: The file {filename} was not found.")
    except Exception as e:
        logging.error(f"Error downloading TikTok video: {str(e)}")

async def convert_video_to_mp3(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='mp3')
    audio_clip.close()
    video_clip.close()

async def download_youtube(url, output_path="downloads", message=None, format="mp4"):
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
        options = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
            }
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')
                filename = f'{output_path}/{title}.mp3'
                print(filename)
                ydl.download([url])
                thumbnail_filename = os.path.join(output_path, f"{info_dict['title']}")

                if os.path.exists(filename) and message:
                    thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

                    # Сохраняем обложку
                    if thumbnail_path:
                        thumbnail_response = requests.get(thumbnail_path)
                        with open(thumbnail_filename, 'wb') as thumbnail_file:
                            thumbnail_file.write(thumbnail_response.content)

                await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(thumbnail_filename))

                os.remove(filename)
                os.remove(thumbnail_filename)

            except Exception as e:
                logging.error(f"Error downloading YouTube Audio: {str(e)}")
                logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")
