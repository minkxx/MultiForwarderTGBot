from pyrogram.errors import PeerIdInvalid


async def get_user_info(c, user_id):
    try:
        user = await c.get_users(user_id)
    except PeerIdInvalid:
        text = f"**⚠️ unable to fetch `{user_id}` info.**"
        return text

    full_name = user.first_name + (user.last_name or "")
    user_id = user.id
    username = user.username
    dc_id = user.dc_id or "1"
    status = str(user.status).split(".")[-1] or "None"
    bot = user.is_bot
    verification = user.is_verified
    scam = user.is_scam
    premium = user.is_premium

    whois_msg = f"""**[{full_name}](tg://user?id={user_id})**
• User id : `{user_id}`
• Username : @{username}
• DC : `{dc_id}`
• Status : `{status}`
• Scam : `{scam}`
• Bot : `{bot}`
• Premium : `{premium}`
• Verified : `{verification}`
"""
    return whois_msg
