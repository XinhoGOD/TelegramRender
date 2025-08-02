import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API de Telegram
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Configuración del userbot
SESSION_NAME = 'userbot_session' 