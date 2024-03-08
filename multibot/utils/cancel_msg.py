async def cancel_in_msg(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the process")
        return True
    elif msg.text.startswith("/"):
        await msg.reply("Cancelled the process")
        return True
