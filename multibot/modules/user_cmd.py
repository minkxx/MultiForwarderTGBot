from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired


from multibot import bot, LOG_GROUP
from multibot.decorators.forcesub import force_sub
from multibot.utils.cancel_msg import cancel_in_msg
from multibot.utils.check_is_channel import bot_not_in_channel
from multibot.database import *


@bot.on_message(filters.command("id"))
async def id(c: bot, m: Message):
    id_text = f"**Chat id of** {m.chat.title} **is** `{m.chat.id}`"
    await c.send_message(
        chat_id=m.chat.id,
        text=id_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("set") & filters.private)
@force_sub
async def sett(c: bot, m: Message):
    await c.send_message(
        chat_id=m.chat.id,
        text=f"**To set up your channels enter** `from_chat_id` **and** `to_chat_id` **when asked!**",
        reply_to_message_id=m.id,
    )

    from_chat_id_msg = await c.ask(
        chat_id=m.chat.id,
        text=f"**Send your** `from_chat_id` **here**\n/cancel - cancel the process.",
    )

    if await cancel_in_msg(from_chat_id_msg):
        return
    elif await bot_not_in_channel(from_chat_id_msg):
        return
    else:
        from_chat_id = int(from_chat_id_msg.text)

    to_chat_id_msg = await c.ask(
        chat_id=m.chat.id,
        text=f"**Send your** `to_chat_id` **here**\n/cancel - cancel the process.",
    )

    if await cancel_in_msg(to_chat_id_msg):
        return
    elif await bot_not_in_channel(to_chat_id_msg):
        return
    else:
        to_chat_id = int(to_chat_id_msg.text)

    set_chat_id(m, from_chat_id, to_chat_id)
    await c.send_message(
        chat_id=m.chat.id,
        text=f"**✅ Successfully set\n**from_chat_id : **`{from_chat_id}` : **to_chat_id : **`{to_chat_id}`",
    )


@bot.on_message(filters.incoming & filters.channel)
async def get_incoming(c: bot, m: Message):
    all_chats = get_all_chats(get_only_value=True)
    for chat in all_chats:
        if m.chat.id == int(chat["from_chat_id"]):
            try:
                await c.copy_message(
                    chat_id=int(chat["to_chat_id"]),
                    from_chat_id=int(chat["from_chat_id"]),
                    message_id=m.id,
                )
            except ChatAdminRequired as err:
                await c.send_message(
                    chat_id=LOG_GROUP,
                    text=f"**⚠️ Bot is not admin on chat :** `{chat['to_chat_id']}`",
                )
