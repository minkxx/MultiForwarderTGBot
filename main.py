import os
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType

from pymongo.mongo_client import MongoClient

if os.path.exists("config.py"):
    from config import *
else:
    from sample_config import *

bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


mongoClient = MongoClient(
    "mongodb+srv://monsur:ag6nNLnj7JsGjft6@multi.sc3totr.mongodb.net/?retryWrites=true&w=majority&appName=multi"
)

collection = mongoClient["chat_ids"]["ids"]

# Database function
def set_chat_id(m: Message, from_chat_id: int, to_chat_id: int):
    user_id = str(m.from_user.id)
    data = {"from_chat_id": int(from_chat_id), "to_chat_id": int(to_chat_id)}
    obj_doc = {user_id: {"$exists": True}}
    obj = collection.find_one(obj_doc)
    if obj:
        all_datas = []
        for i in obj[user_id]:
            all_datas.append(i)
        if data not in all_datas:
            all_datas.append(data)
        updateQuery = {"$set": {user_id: all_datas}}
        collection.update_one(obj_doc, updateQuery)
    else:
        data = [{"from_chat_id": from_chat_id, "to_chat_id": to_chat_id}]
        toSendDoc = {user_id: data}
        collection.insert_one(toSendDoc)


def get_all_chats():
    all_documents = collection.find()
    all_ = []
    all_chats = []

    for document in all_documents:
        last_key, last_value = list(document.items())[-1]
        all_.append(last_value)
    for i in all_:
        for j in i:
            all_chats.append(j)
    return all_chats


@bot.on_message(filters.command("start"))
async def start(c: bot, m: Message):
    me = await c.get_me()
    start_text = f"Hey! {m.from_user.mention}, welcome to @{me.username}.\nI'm a simple message forwarder bot from channel to channel based with Pyrogram.\nAny bugs? Report to developer.\n\nTo know more /help\n\nDeveloped by @minkxx69."
    await c.send_message(
        chat_id=m.chat.id,
        text=start_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("help"))
async def help(c: bot, m: Message):
    me = await c.get_me()
    help_text = f"**Help Menu - {me.username}**\n\nTo configure message forwarding from one channel to another you need to set two vars.\n\n**from_chat_id** : Chat id of the channel from which you want to forward message.\n**to_chat_id** : Chat id of the channel to which you want to forward your messages.\n\nAdd this bot to both your channel with admin rights and type `/id` to get id of the channels then return here and type `/set from_chat_id to_chat_id` replace from_chat_id and to_chat_id with your chat ids\n\nIf everything goes right you're all done."
    await c.send_message(
        chat_id=m.chat.id,
        text=help_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("id"))
async def id(c: bot, m: Message):
    id_text = f"Chat id of {m.chat.title} is `{m.chat.id}`"
    await c.send_message(
        chat_id=m.chat.id,
        text=id_text,
        reply_to_message_id=m.id,
    )


@bot.on_message(filters.command("set"))
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


@bot.on_message(filters.incoming)
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


if __name__ == "__main__":
    print("Bot Alive!!")
    bot.start()
    bot.send_message(LOG_GROUP, "Bot is Alive!!")
    idle()
    
