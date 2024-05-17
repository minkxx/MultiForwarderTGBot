import os
from dotenv import load_dotenv

from pyromod import Client


load_dotenv()


VERSION = "0.1.2"


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
LOG_GROUP = int(os.getenv("LOG_GROUP"))
ADMIN_USERS_ID = [int(user_id) for user_id in os.getenv("ADMIN_USERS_ID").split()]
FORCE_SUB_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL"))


if not API_ID:
    print("'API_ID' missing!")
    exit()
if not API_HASH:
    print("'API_HASH' missing!")
    exit()
if not BOT_TOKEN:
    print("'BOT_TOKEN' missing!")
    exit()
if not MONGO_DB_URI:
    print("'MONGO_DB_URI' missing!")
    exit()
if not LOG_GROUP:
    print("'LOG_GROUP' missing!")
    exit()
if not ADMIN_USERS_ID:
    print("'ADMIN_USERS_ID' missing!")
    exit()
if not FORCE_SUB_CHANNEL:
    print("'FORCE_SUB_CHANNEL' missing!")
    exit()


bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

bot.start()
me = bot.get_me()
BOT_USERNAME = me.username
BOT_NAME = me.full_name

from multibot.modules import *
