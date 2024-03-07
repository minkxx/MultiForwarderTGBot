from functools import wraps

from pyrogram.types import Message

from multibot import FORCE_SUB_CHANNEL
from multibot.database import add_user_db


async def you_must_join(client, m):
    await client.send_message(
        chat_id=m.chat.id,
        text=f"Must join @channel to use this bot.\nJoin and start bot again.",
        reply_to_message_id=m.id,
    )


def force_sub(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        members = [
            mem.user.id async for mem in client.get_chat_members(FORCE_SUB_CHANNEL)
        ]
        print(members)
        add_user_db(message.from_user.id)
        if message.from_user.id in members:
            return await func(client, message, *args, **kwargs)
        else:
            return await you_must_join(client, message, *args, **kwargs)

    return wrapper
