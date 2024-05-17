from pyrogram import filters
from pyrogram.types import Message

from multibot import bot, LOG_GROUP
from multibot.decorators.owner_only import owner
from multibot.utils.get_user_info import get_user_info
from multibot.database import *


blocked_chats = []


@bot.on_message(filters.command("admin_help") & filters.private)
@owner
async def admin_help(c: bot, m: Message):
    help_text = f"""**⚙️ Admin Help Menu**

💬 /broadcast - reply to a message or media to broadcast it to all users.

💬 /stats - get all currently used users.

💬 /get_user_chats __user_id__ - get all configured chats of the user id.

💬 /config_users_info - sends all configured users info.

💬 /remove_blocked_users - remove users from db that have blocked this bot.

💬 /user_chats_link __chat_id__ - get invite links for all configured chats."""
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
        msg = await c.send_message(chat_id=m.chat.id, text="`Starting broadcast..`")
        all_users = get_all_users()
        done_count = 0
        error_count = 0
        error_text = f"**⚠️ Unable! to broadcast on these chats **"
        for user_id in all_users:
            await msg.edit_text(f"Sending broadcast to user: `{user_id}`")
            try:
                await c.copy_message(
                    chat_id=user_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.id,
                )
                done_count += 1
                await msg.edit_text(f"Broadcast sent to user: `{user_id}`")
            except Exception as e:
                error_text += f"\n `{user_id}`"
                blocked_chats.append(user_id)
                error_count += 1
                await msg.edit_text(f"Unable broadcast to user: `{user_id}`")
        else:
            await msg.delete()
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


@bot.on_message(filters.command("user_chats_link") & filters.private)
@owner
async def user_chats_link(c: bot, m: Message):
    msg = await c.send_message(
            chat_id=m.chat.id, 
            text="__Fetching links please wait...__"
        )
    chats_list = [chat[chat_id] for chat in get_all_chats(get_only_value=True) for chat_id in chat]
    if len(m.command) <= 1:
        join_text = "Here are the links:\n\n"
        for chat_id in chats_list:
            try:
                join_link = await c.export_chat_invite_link(chat_id)
                join_text += f"{join_link}\n"
            except Exception as e:
                join_text += f"unable to fetch invite link: `{chat_id}`\n"
                continue
        
        await c.send_message(
            chat_id=m.chat.id, text=join_text, disable_web_page_preview=True
        )
    else:
        user_chat_id = int(m.command[1])
        join_text = ""

        if user_chat_id in chats_list:
            try:
                join_link = await c.export_chat_invite_link(user_chat_id)
                join_text += f"Here's the chat invite link for chat:`{user_chat_id}`\n\n{join_link}"
            except Exception as e:
                join_text += f"Unable to fetch invite link: `{user_chat_id}`\n\nError:\n```{e}```"
            await c.send_message(
                chat_id=m.chat.id, text=join_text, disable_web_page_preview=True
            )
        else:
            await c.send_message(
                chat_id=m.chat.id, text=f"'`{user_chat_id}`' is not a configured chat!"
            )
    

    await msg.delete()
