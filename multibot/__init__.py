import os

from pyromod import Client

if os.path.exists("config.py"):
    from config import *
else:
    from sample_config import *

VERSION = "0.0.3"

bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

bot.start()
me = bot.get_me()
BOT_USERNAME = me.username

from multibot.modules import *
