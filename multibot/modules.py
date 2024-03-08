from pyrogram import filters
from pyrogram.types import Message

from multibot import bot, BOT_USERNAME, LOG_GROUP
from multibot.database import set_chat_id, get_all_chats, get_all_users, add_user_db
from multibot.decorators.forcesub import force_sub
from multibot.decorators.owner_only import owner
from multibot.utils.cancel_msg import cancel_in_msg
from multibot.utils.check_media_type import check_and_send


@bot.on_message(filters.command("start") & filters.private)
async def start(c: bot, m: Message):
    add_user_db(m.from_user.id)
    start_text = f"""Hey! 🩷 {m.from_user.mention}, welcome to @{BOT_USERNAME}.

**I'm a simple message forwarder bot from channel to channel based with pyrogram.
Any bugs? Report to developer.**

To know more /help

Developed with 🩵 @minkxx69.
Powered by @nrbots"""
    await c.send_message(
        chat_id=m.chat.id,
        text=start_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("help") & filters.private)
async def help(c: bot, m: Message):
    help_text = f"""**Help Menu - {BOT_USERNAME} 🤖**

**🔧 To configure message forwarding from one channel to another you need to set two vars.**
- **from_chat_id** : Chat id of the channel from which you want to forward message.
- **to_chat_id** : Chat id of the channel to which you want to forward your messages.

**⚙️ Add this bot to both your channel with admin rights and type `/id` to get id of the channels then return here and type /set

Enter `from_chat_id` and `to_chat_id` when asked.

**If everything goes well you're all done 🤩**"""
    await c.send_message(
        chat_id=m.chat.id,
        text=help_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("id"))
async def id(c: bot, m: Message):
    id_text = f"**Chat id of** {m.chat.title} **is** `{m.chat.id}`"
    await c.send_message(
        chat_id=m.chat.id,
        text=id_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("set") & filters.private)
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
    else:
        from_chat_id = int(from_chat_id_msg.text)

    to_chat_id_msg = await c.ask(
        chat_id=m.chat.id,
        text=f"**Send your** `to_chat_id` **here**\n/cancel - cancel the process.",
    )

    if await cancel_in_msg(to_chat_id_msg):
        return
    else:
        to_chat_id = int(to_chat_id_msg.text)

    set_chat_id(m, from_chat_id, to_chat_id)
    await c.send_message(
        chat_id=m.chat.id,
        text=f"**✅ Successfully set\n**from_chat_id : **`{from_chat_id}` : **to_chat_id : **`{to_chat_id}`",
    )


@bot.on_message(filters.command("broadcast"))
@owner
async def broadcast(c: bot, m: Message):
    cmd = m.command
    if not m.reply_to_message:
        await c.send_message(
            chat_id=m.chat.id,
            text="Please reply to a message to broadcast!!",
            reply_to_message_id=m.id,
        )
    else:
        all_users = get_all_users()
        done_count = 0
        error_count = 0
        for user_id in all_users:
            try:
                await check_and_send(m.reply_to_message, c, user_id)
                done_count += 1
            except Exception as e:
                text = f"**Error!** while broadcasting message to user id : `{user_id}`"
                await c.send_message(chat_id=m.chat.id, text=text)
                error_count += 1
        else:
            await c.send_message(
                chat_id=m.chat.id,
                text=f"**Successfully** broadcasted message to {done_count} chats out of {len(all_users)}.\n**Error** {error_count} chats",
            )


# todo : return every user in database to log group
@bot.on_message(filters.command("stats"))
@owner
async def stats(c: bot, m: Message):
    all_users = get_all_users()
    send_text = f"**Total** `{len(all_users)}` **users have used this bot so far.**\nListing all users ::>\n"
    await c.send_message(
        chat_id=m.chat.id,
        text=f"Total `{len(all_users)}` users have used this bot so far.",
        reply_to_message_id=m.id,
    )
    for i in all_users:
        send_text += f"\n- `{i}`"

    await c.send_message(
        chat_id=LOG_GROUP,
        text=send_text,
    )


@bot.on_message(filters.incoming & filters.channel)
async def get_incoming(c: bot, m: Message):
    all_chats = get_all_chats()
    for chat in all_chats:
        if m.chat.id == int(chat["from_chat_id"]):
            await check_and_send(m, c, int(chat["to_chat_id"]))
