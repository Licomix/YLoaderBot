# Файл с секретными данными (токены, ключи и т.д.)
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

spotify_client_id = os.getenv('client_id')
spotify_secret = os.getenv('secret')
