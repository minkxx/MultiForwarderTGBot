from pyrogram import filters
from pyrogram import __version__ as PYRO_VERSION
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.errors import ChatAdminRequired

from multibot import bot, BOT_USERNAME, LOG_GROUP, VERSION, BOT_NAME
from multibot.database import (
    set_chat_id,
    get_all_chats,
    get_all_users,
    chats_of_user,
    remove_user_db,
    remove_chat_id,
)
from multibot.decorators.forcesub import force_sub
from multibot.decorators.owner_only import owner
from multibot.utils.cancel_msg import cancel_in_msg
from multibot.utils.get_user_info import get_user_info
from multibot.utils.check_is_channel import bot_not_in_channel

global blocked_chats
blocked_chats = []

start_text = """Hey! 🩷 {}, welcome to @{}.

**I'm a simple message forwarder bot from channel to channel based with pyrogram.
Any bugs? Report to developer.**

Developed with 🩵
- @minkxx69"""

home_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Help", callback_data="help_data"),
            InlineKeyboardButton(text="About", callback_data="about_data"),
        ],
        [
            InlineKeyboardButton(text="Your Chats", callback_data="your_chats_data"),
            InlineKeyboardButton(text="Set Chat", callback_data="set_chat_data"),
        ],
        [
            InlineKeyboardButton(
                text="Github Repo", url="https://github.com/minkxx/MultiForwarderTgBot"
            )
        ],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

help_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Home", callback_data="home_data"),
            InlineKeyboardButton(text="About", callback_data="about_data"),
        ],
        [
            InlineKeyboardButton(text="Your Chats", callback_data="your_chats_data"),
            InlineKeyboardButton(text="Set Chat", callback_data="set_chat_data"),
        ],
        [
            InlineKeyboardButton(
                text="Github Repo", url="https://github.com/minkxx/MultiForwarderTgBot"
            )
        ],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)

about_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Home", callback_data="home_data"),
            InlineKeyboardButton(text="Help", callback_data="help_data"),
        ],
        [
            InlineKeyboardButton(text="Your Chats", callback_data="your_chats_data"),
            InlineKeyboardButton(text="Set Chat", callback_data="set_chat_data"),
        ],
        [
            InlineKeyboardButton(
                text="Github Repo", url="https://github.com/minkxx/MultiForwarderTGBot"
            )
        ],
        [InlineKeyboardButton(text="Close", callback_data="close_data")],
    ]
)


delete_chats_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="Delete Chat", callback_data="delete_chat_data")],
        [InlineKeyboardButton(text="Close", callback_data="home_data")]
    ]
)


# Commands for all users
@bot.on_message(filters.command("start") & filters.private)
@force_sub
async def start(c: bot, m: Message):
    global start_text
    start_text = start_text.format(m.from_user.full_name, BOT_USERNAME)
    await c.send_message(
        chat_id=m.chat.id,
        text=start_text,
        reply_to_message_id=m.id,
        reply_markup=home_keyboard,
    )


# Callback datas


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
        await c.send_message(chat_id=cbq.message.chat.id, text=chat_text, reply_markup=delete_chats_keyboard)
    else:
        await c.send_message(
            chat_id=cbq.message.chat.id,
            text="You haven't configured any chat yet!"
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
    chat_msg = await c.ask(
        chat_id=cbq.message.chat.id,
        text=f"**Enter your chat serial no to delete**\n/cancel - cancel the process.",
    )
    if await cancel_in_msg(chat_msg):
        return
    elif not chat_msg.text.isdigit():
        return
    else:
        chat_index = int(chat_msg.text)

    deleted_chat = remove_chat_id(cbq.from_user.id, chat_index-1)
    if deleted_chat:
        await cbq.message.edit(text=f"**Deleted**\n{chat_index}. from_chat_id:{deleted_chat['from_chat_id']} - to_chat_id:{deleted_chat['from_chat_id']}")
    else:
        await c.send_message(chat_id=cbq.message.chat.id, text=f"'{chat_index}' is not valid serial no!")

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
                    message_id = m.id
                    )
            except ChatAdminRequired as err:
                await c.send_message(
                    chat_id=LOG_GROUP,
                    text=f"**⚠️ Bot is not admin on chat :** `{chat['to_chat_id']}`",
                )


# Commands for admins
@bot.on_message(filters.command("admin_help") & filters.private)
@owner
async def admin_help(c: bot, m: Message):
    help_text = f"""**⚙️ Admin Help Menu**

💬 /broadcast - reply to a message or media to broadcast it to all users.

💬 /stats - get all currently used users.

💬 /get_user_chats __user_id__ - get all configured chats of the user id.

💬 /config_users_info - sends all configured users info.

💬 /remove_blocked_users - remove users from db that have blocked this bot."""
    await c.send_message(
        chat_id=m.chat.id,
        text=help_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("broadcast") & filters.private)
@owner
async def broadcast(c: bot, m: Message):
    if not m.reply_to_message:
        await c.send_message(
            chat_id=m.chat.id,
            text="**⚠️ Please reply to a message to broadcast!!**",
            reply_to_message_id=m.id,
        )
    else:
        all_users = get_all_users()
        done_count = 0
        error_count = 0
        error_text = f"**⚠️ Unable! to broadcast on these chats **"
        for user_id in all_users:
            try:
                await c.copy_message(
                    chat_id=user_id,
                    from_chat_id=m.chat.id,
                    message_id = m.id
                )
                done_count += 1
            except Exception as e:
                error_text += f"\n `{user_id}`"
                blocked_chats.append(user_id)
                error_count += 1
        else:
            await c.send_message(
                chat_id=m.chat.id,
                text=f"**✅ Successfully** broadcasted message to {done_count} chats out of {len(all_users)}.\n**⚠️ Error** {error_count} chats",
            )
        if error_count:
            await c.send_message(chat_id=m.chat.id, text=error_text)


@bot.on_message(filters.command("remove_blocked_users") & filters.private)
@owner
async def remove_blocked_users(c: bot, m: Message):
    if len(blocked_chats) != 0:
        x = await c.send_message(
            chat_id=m.chat.id,
            text="__Removing blocked users...__",
        )
        all_users = get_all_users()
        for user_id in all_users:
            if user_id in blocked_chats:
                remove_user_db(user_id)
        await x.edit_text("**✅ Done**")
    else:
        await c.send_message(
            chat_id=m.chat.id,
            text="**⚠️ List is empty. Please gather blocked user first!!**",
        )


@bot.on_message(filters.command("stats") & filters.private)
@owner
async def stats(c: bot, m: Message):
    cmd = m.command
    all_users = get_all_users()
    all_configured_users = get_all_chats(get_only_key=True)

    send_text = f"**Total** `{len(all_users)}` **users have used this bot so far.\n\n**Listing users that have configured chats :\n"
    for i in all_configured_users:
        send_text += f"\n- `{i}`"

    if len(cmd) == 1:
        await c.send_message(
            chat_id=m.chat.id,
            text=send_text,
            reply_to_message_id=m.id,
        )
    else:
        x = await c.send_message(
            chat_id=m.chat.id,
            text=f"**Sending** __stats__ **to log group...**",
            reply_to_message_id=m.id,
        )
        await c.send_message(
            chat_id=LOG_GROUP,
            text=send_text,
        )
        await x.edit_text("**Sent!!**")


@bot.on_message(filters.command("get_user_chats") & filters.private)
@owner
async def get_user_chats(c: bot, m: Message):
    cmd = m.command
    if len(cmd) > 1:
        all_chats = chats_of_user(cmd[1])
        if all_chats:
            text = f"**⚙️ Chats set by** {cmd[1]} :\n\n"
            for chat in all_chats:
                text += f"🔧 from_chat `{chat['from_chat_id']}` : to_chat `{chat['to_chat_id']}`\n"
            await c.send_message(
                chat_id=m.chat.id,
                text=text,
                reply_to_message_id=m.id,
            )
        else:
            await c.send_message(
                chat_id=m.chat.id,
                text=f"**User** `{cmd[1]}` **have not set any chat yet!!**",
                reply_to_message_id=m.id,
            )
    else:
        await c.send_message(
            chat_id=m.chat.id,
            text="**⚠️ Please fill** __user_id__ **argument!!**",
            reply_to_message_id=m.id,
        )


@bot.on_message(filters.command("config_users_info") & filters.private)
@owner
async def get_all_configured_users_info(c: bot, m: Message):
    x = await c.send_message(
        chat_id=m.chat.id,
        text="👨🏻‍💻 __sending infos__",
        reply_to_message_id=m.id,
    )

    all_configured_users = get_all_chats(get_only_key=True)

    for user_id in all_configured_users:
        msg = await get_user_info(c, user_id)
        await c.send_message(
            chat_id=m.chat.id,
            text=msg,
        )

    await x.edit_text("**✅ Sent!!**")
