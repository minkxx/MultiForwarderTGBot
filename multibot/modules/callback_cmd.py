from pyrogram import filters
from pyrogram import __version__ as PYRO_VERSION
from pyrogram.types import Message, CallbackQuery

from multibot import bot, BOT_USERNAME, BOT_NAME, VERSION
from multibot.utils.keyboards import *
from multibot.utils.ikb import ikb
from multibot.utils.cancel_msg import cancel_in_msg
from multibot.utils.check_is_channel import bot_not_in_channel
from multibot.database import *
from multibot.decorators.forcesub import force_sub


@bot.on_message(filters.command("start") & filters.private)
@force_sub
async def start(c: bot, m: Message):
    global start_text
    start_text = f"""Hey! 🩷 {m.from_user.full_name}, welcome to @{BOT_USERNAME}.

**I'm a simple message forwarder bot from channel to channel based with pyrogram.
Any bugs? Report to developer.**

Developed with 🩵
- @minkxx69"""
    await c.send_message(
        chat_id=m.chat.id,
        text=start_text,
        reply_to_message_id=m.id,
        reply_markup=home_keyboard,
    )


@bot.on_callback_query(filters.regex("home_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    await cbq.message.edit(text=start_text, reply_markup=home_keyboard)


@bot.on_callback_query(filters.regex("help_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    help_text = f"""**Help Menu - {BOT_USERNAME} 🤖**
    
**🔧 To configure message forwarding from one channel to another you need to set two vars.**
- **from_chat_id** : Chat id of the channel from which you want to forward message.
- **to_chat_id** : Chat id of the channel to which you want to forward your messages.

**⚙️ Add this bot to both your channel with admin rights and type `/id` to get id of the channels then return here and type /set

Enter `from_chat_id` and `to_chat_id` when asked.

**If everything goes well you're all done 🤩**"""

    await cbq.message.edit(text=help_text, reply_markup=help_keyboard)


@bot.on_callback_query(filters.regex("about_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    about_text = f"""**🤖 Bot Name :** `{BOT_NAME}`
**🛠 Bot Version :** `{VERSION}`
**⚒ Pyrogram Version :** `{PYRO_VERSION}`

**Powered by ~** ❤️ @nrbots

**Developed by ~** 🩵 @minkxx69
"""
    await cbq.message.edit(text=about_text, reply_markup=about_keyboard)


@bot.on_callback_query(filters.regex("close_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    await cbq.message.delete()


@bot.on_callback_query(filters.regex("your_chats_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    all_chats = chats_of_user(cbq.from_user.id)
    if all_chats and len(all_chats) != 0:
        chat_text = "**Your Configured Chats**\n\n"
        count = 1
        if all_chats:
            for chat in all_chats:
                chat_text += f"{count}. 🔧 from_chat `{chat['from_chat_id']}` : to_chat `{chat['to_chat_id']}`\n\n"
                count += 1
        await cbq.message.edit(text=chat_text, reply_markup=delete_chats_keyboard)

    else:
        await cbq.message.edit(
            text="You haven't configured any chat yet!", reply_markup=close_keyboard
        )


@bot.on_callback_query(filters.regex("set_chat_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    await c.send_message(
        chat_id=cbq.message.chat.id,
        text=f"**To set up your channels enter** `from_chat_id` **and** `to_chat_id` **when asked!**",
    )

    from_chat_id_msg = await c.ask(
        chat_id=cbq.message.chat.id,
        text=f"**Send your** `from_chat_id` **here**\n/cancel - cancel the process.",
    )

    if await cancel_in_msg(from_chat_id_msg):
        return
    elif await bot_not_in_channel(from_chat_id_msg):
        return
    else:
        from_chat_id = int(from_chat_id_msg.text)

    to_chat_id_msg = await c.ask(
        chat_id=cbq.message.chat.id,
        text=f"**Send your** `to_chat_id` **here**\n/cancel - cancel the process.",
    )

    if await cancel_in_msg(to_chat_id_msg):
        return
    elif await bot_not_in_channel(to_chat_id_msg):
        return
    else:
        to_chat_id = int(to_chat_id_msg.text)

    set_chat_id(cbq, from_chat_id, to_chat_id)
    await c.send_message(
        chat_id=cbq.message.chat.id,
        text=f"**✅ Successfully set\n**from_chat_id : **`{from_chat_id}` : **to_chat_id : **`{to_chat_id}`",
    )


@bot.on_callback_query(filters.regex("delete_chat_data"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    global buttons_dict
    buttons_dict = {}

    all_chats = chats_of_user(cbq.from_user.id)
    if all_chats and len(all_chats) != 0:
        chat_text = "**Select the button below according to your chat serial no. to delete.**\n\n"
        count = 1
        if all_chats:
            for chat in all_chats:
                chat_text += f"{count}. 🔧 from_chat `{chat['from_chat_id']}` : to_chat `{chat['to_chat_id']}`\n\n"
                buttons_dict[f"{count}"] = f"delete=index={count-1}"
                count += 1

        del_keyboard = ikb(buttons_dict, 6)
        await cbq.message.edit(text=chat_text, reply_markup=del_keyboard)


@bot.on_callback_query(filters.regex(pattern="^(delete=index=.*)$"))
async def help_cmd(c: bot, cbq: CallbackQuery):
    chat_index = int(cbq.data.split("=")[-1])
    deleted_chat = remove_chat_id(cbq.from_user.id, chat_index)
    await cbq.message.edit(
        text=f"**Deleted**\n{chat_index+1}. from_chat_id:{deleted_chat['from_chat_id']} - to_chat_id:{deleted_chat['from_chat_id']}",
        reply_markup=close_keyboard,
    )
