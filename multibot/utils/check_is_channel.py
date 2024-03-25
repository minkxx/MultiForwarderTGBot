from pyrogram.enums import ChatType
from pyrogram.errors import ChannelInvalid

from multibot import bot

async def bot_not_in_channel(msg):
    try:
        chat = await bot.get_chat(int(msg.text))
        if chat:
            if (chat.type == ChatType.PRIVATE) or (chat.type == ChatType.BOT) or (chat.type == ChatType.GROUP) or (chat.type == ChatType.SUPERGROUP):
                await bot.send_message(
                chat_id=msg.chat.id,
                text="**Please enter a channel id only!!**"
                )
                return True
            elif chat.type == ChatType.CHANNEL:
                return False
        else:
            await bot.send_message(
                chat_id=msg.chat.id,
                text="**Please add bot to your channel first!!**"
                )
            return True
    except (ChannelInvalid) as e:
        await bot.send_message(
            chat_id=msg.chat.id,
            text="**Please add bot to your channel first!!**"
            )
        return True