from functools import wraps

from pyrogram.types import Message

from multibot import OWNER_ID


async def you_aint_owner(client, m):
    await client.send_message(
        chat_id=m.chat.id,
        text=f"You ain't **Owner** to do this!!",
        reply_to_message_id=m.id,
    )


def owner(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.from_user and message.from_user.id == OWNER_ID:
            return await func(client, message, *args, **kwargs)
        else:
            return await you_aint_owner(client, message, *args, **kwargs)

    return wrapper
