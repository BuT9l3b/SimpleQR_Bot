import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Bot settings
BOT_TOKEN = os.getenv('BOT_TOKEN')

# QR code settings
QR_VERSION = 1
QR_ERROR_CORRECTION = 'H'
QR_BOX_SIZE = 10
QR_BORDER = 4
