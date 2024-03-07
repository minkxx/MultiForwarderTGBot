from functools import wraps

from pyrogram.types import Message

from multibot import FORCE_SUB_CHANNEL


async def you_must_join(client, m):
    chat_info = await client.get_chat(FORCE_SUB_CHANNEL)
    JOIN_TEXT = ""
    if chat_info.username:
        JOIN_TEXT = f"Must join @{chat_info.username} to use this bot.\nJoin and start bot again."
    else:
        CHAT_NAME = chat_info.title
        JOIN_TEXT = f"Must join [{CHAT_NAME}]({chat_info.invite_link}) to use this bot.\nJoin and start bot again."
    await client.send_message(
        chat_id=m.chat.id,
        text=JOIN_TEXT,
        reply_to_message_id=m.id,
    )


def force_sub(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        members = [
            mem.user.id async for mem in client.get_chat_members(FORCE_SUB_CHANNEL)
        ]
        if message.from_user.id in members:
            return await func(client, message, *args, **kwargs)
        else:
            return await you_must_join(client, message, *args, **kwargs)

    return wrapper
