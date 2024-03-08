from pyrogram.enums import MessageMediaType


async def check_and_send(m, c, to_chat_id):
    if m.text:
        await c.send_message(
            chat_id=to_chat_id,
            text=m.text,
        )

    elif m.media == MessageMediaType.ANIMATION:
        if m.caption:
            text = m.caption
        else:
            text = ""

        await c.send_animation(
            chat_id=to_chat_id,
            animation=m.animation.file_id,
            caption=text,
        )

    elif m.media == MessageMediaType.AUDIO:
        if m.caption:
            text = m.caption
        else:
            text = ""

        await c.send_audio(
            chat_id=to_chat_id,
            audio=m.audio.file_id,
            caption=text,
        )

    elif m.media == MessageMediaType.DOCUMENT:
        if m.caption:
            text = m.caption
        else:
            text = ""

        await c.send_document(
            chat_id=to_chat_id,
            document=m.document.file_id,
            caption=text,
        )

    elif m.media == MessageMediaType.PHOTO:
        if m.caption:
            text = m.caption
        else:
            text = ""

        await c.send_photo(
            chat_id=to_chat_id,
            photo=m.photo.file_id,
            caption=text,
        )

    elif m.media == MessageMediaType.STICKER:
        await c.send_sticker(
            chat_id=to_chat_id,
            sticker=m.sticker.file_id,
        )

    elif m.media == MessageMediaType.VIDEO:
        if m.caption:
            text = m.caption
        else:
            text = ""

        await c.send_video(
            chat_id=to_chat_id,
            video=m.video.file_id,
            caption=text,
        )

    elif m.media == MessageMediaType.VOICE:
        if m.caption:
            text = m.caption
        else:
            text = ""

        await c.send_voice(
            chat_id=to_chat_id,
            voice=m.voice.file_id,
            caption=text,
        )

    elif m.media == MessageMediaType.VIDEO_NOTE:
        await c.send_video_note(
            chat_id=to_chat_id,
            video_note=m.video_note.file_id,
        )

    elif m.media == MessageMediaType.LOCATION:
        await c.send_location(
            chat_id=to_chat_id,
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
            chat_id=to_chat_id,
            question=m.poll.question,
            options=[q["text"] for q in m.poll.options],
            type=m.poll.type,
            allows_multiple_answers=allow,
            longitude=m.location.longitude,
        )

    elif m.media == MessageMediaType.DICE:
        await c.send_dice(
            chat_id=to_chat_id,
            emoji=m.dice.emoji,
        )

    else:
        print("Unknown message type!")
