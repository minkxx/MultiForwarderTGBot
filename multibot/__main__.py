import asyncio

from pyrogram import idle
from multibot import bot, LOG_GROUP


loop = asyncio.get_event_loop()


async def start_bot():
    print("Sending online status!")
    await bot.send_message(LOG_GROUP, "Bot Online!")
    print("Sent!")
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(start_bot())
