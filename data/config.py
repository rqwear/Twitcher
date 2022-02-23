import os
from dotenv import load_dotenv
'''
Для запуска необходимо создать файл .env
в котором указать все необходимые токены и ip
BOT_TOKEN = 
ip = 
TWITCH_ID=
TWITCH_SECRET=
'''

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [int(os.getenv("BOT_OWNER"))
]
# Postgresql data
DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_NAME = str(os.getenv("DB_NAME"))
DB_HOST = str(os.getenv("DB_HOST"))


ip = os.getenv("ip")

TWITCH_ID = str(os.getenv("TWITCH_ID"))
TWITCH_SECRET = str(os.getenv("TWITCH_SECRET"))
BOT_OWNER = int(os.getenv("BOT_OWNER"))

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
