from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType

from multibot import bot, BOT_USERNAME
from multibot.database import set_chat_id, get_all_chats, get_all_users
from multibot.decorators.forcesub import force_sub
from multibot.decorators.owner_only import owner


@bot.on_message(filters.command("start") & filters.private)
@force_sub
async def start(c: bot, m: Message):
    start_text = f"Hey! {m.from_user.mention}, welcome to @{BOT_USERNAME}.\nI'm a simple message forwarder bot from channel to channel based with Pyrogram.\nAny bugs? Report to developer.\n\nTo know more /help\n\nDeveloped by @minkxx69."
    await c.send_message(
        chat_id=m.chat.id,
        text=start_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("help") & filters.private)
@force_sub
async def help(c: bot, m: Message):
    help_text = f"**Help Menu - {BOT_USERNAME}**\n\nTo configure message forwarding from one channel to another you need to set two vars.\n\n**from_chat_id** : Chat id of the channel from which you want to forward message.\n**to_chat_id** : Chat id of the channel to which you want to forward your messages.\n\nAdd this bot to both your channel with admin rights and type `/id` to get id of the channels then return here and type `/set from_chat_id to_chat_id` replace from_chat_id and to_chat_id with your chat ids\n\nIf everything goes right you're all done."
    await c.send_message(
        chat_id=m.chat.id,
        text=help_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("id") & filters.private)
@force_sub
async def id(c: bot, m: Message):
    id_text = f"Chat id of {m.chat.title} is `{m.chat.id}`"
    await c.send_message(
        chat_id=m.chat.id,
        text=id_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("set") & filters.private)
@force_sub
async def sett(c: bot, m: Message):
    cmd = m.command
    if len(cmd) != 3:
        await c.send_message(
            chat_id=m.chat.id,
            text="Please provide only `/set from_chat_id to_chat_id`",
            reply_to_message_id=m.id,
        )
    else:
        set_chat_id(m, cmd[1], cmd[2])
        await c.send_message(
            chat_id=m.chat.id,
            text=f"Success!! set from_chat_id:{cmd[1]} - to_chat_id:{cmd[2]}",
            reply_to_message_id=m.id,
        )


@bot.on_message(filters.command("broadcast"))
@owner
async def broadcast(c: bot, m: Message):
    cmd = m.command
    if len(cmd) < 2:
        await c.send_message(
            chat_id=m.chat.id,
            text="Please provide a message to broadcast!!",
            reply_to_message_id=m.id,
        )
    else:
        all_users = get_all_users()
        for user_id in all_users:
            await c.send_message(
                chat_id=user_id,
                text=" ".join(cmd[1:]),
            )


@bot.on_message(filters.command("stats"))
@owner
async def stats(c: bot, m: Message):
    all_users = get_all_users()
    await c.send_message(
        chat_id=m.chat.id,
        text=f"Total `{len(all_users)}` users have used this bot so far.",
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.incoming & filters.channel)
async def get_incoming(c: bot, m: Message):
    all_chats = get_all_chats()

    for chat in all_chats:
        if m.chat.id == int(chat["from_chat_id"]):

            if m.text:
                await c.send_message(
                    chat_id=int(chat["to_chat_id"]),
                    text=m.text,
                )

            elif m.media == MessageMediaType.ANIMATION:
                if m.caption:
                    text = m.caption
                else:
                    text = ""

                await c.send_animation(
                    chat_id=int(chat["to_chat_id"]),
                    animation=m.animation.file_id,
                    caption=text,
                )

            elif m.media == MessageMediaType.AUDIO:
                if m.caption:
                    text = m.caption
                else:
                    text = ""

                await c.send_audio(
                    chat_id=int(chat["to_chat_id"]),
                    audio=m.audio.file_id,
                    caption=text,
                )

            elif m.media == MessageMediaType.DOCUMENT:
                if m.caption:
                    text = m.caption
                else:
                    text = ""

                await c.send_document(
                    chat_id=int(chat["to_chat_id"]),
                    document=m.document.file_id,
                    caption=text,
                )

            elif m.media == MessageMediaType.PHOTO:
                if m.caption:
                    text = m.caption
                else:
                    text = ""

                await c.send_photo(
                    chat_id=int(chat["to_chat_id"]),
                    photo=m.photo.file_id,
                    caption=text,
                )

            elif m.media == MessageMediaType.STICKER:
                await c.send_sticker(
                    chat_id=int(chat["to_chat_id"]),
                    sticker=m.sticker.file_id,
                )

            elif m.media == MessageMediaType.VIDEO:
                if m.caption:
                    text = m.caption
                else:
                    text = ""

                await c.send_video(
                    chat_id=int(chat["to_chat_id"]),
                    video=m.video.file_id,
                    caption=text,
                )

            elif m.media == MessageMediaType.VOICE:
                if m.caption:
                    text = m.caption
                else:
                    text = ""

                await c.send_voice(
                    chat_id=int(chat["to_chat_id"]),
                    voice=m.voice.file_id,
                    caption=text,
                )

            elif m.media == MessageMediaType.VIDEO_NOTE:
                await c.send_video_note(
                    chat_id=int(chat["to_chat_id"]),
                    video_note=m.video_note.file_id,
                )

            elif m.media == MessageMediaType.LOCATION:
                await c.send_location(
                    chat_id=int(chat["to_chat_id"]),
                    latitude=m.location.latitude,
                    longitude=m.location.longitude,
                )

            elif m.media == MessageMediaType.POLL:
                # TODO : Needs to complete
                if m.poll.allows_multiple_answers:
                    allow = True
                else:
                    allow = False
                await c.send_poll(
                    chat_id=int(chat["to_chat_id"]),
                    question=m.poll.question,
                    options=[q["text"] for q in m.poll.options],
                    type=m.poll.type,
                    allows_multiple_answers=allow,
                    longitude=m.location.longitude,
                )

            elif m.media == MessageMediaType.DICE:
                await c.send_dice(
                    chat_id=int(chat["to_chat_id"]),
                    emoji=m.dice.emoji,
                )

            else:
                print("Unknown message type!")
