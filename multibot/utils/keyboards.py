from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
        [InlineKeyboardButton(text="Back", callback_data="home_data")],
    ]
)

close_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="Back", callback_data="home_data")]]
)
