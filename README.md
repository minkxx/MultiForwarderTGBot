# MultiForwarderTGBot

MultiForwarderTGBot is a Telegram bot designed to forward messages from multiple channels to a single destination. This bot helps you manage and consolidate messages efficiently.

### Features
- Forward messages from multiple channels to a single destination.
- Easy to configure and use.
- Supports various message types including text, images, and files.

### Get it [Here](https://t.me/MultiForwarderRoBot)

## Setup Instructions 

### Prerequisites
- Python 3.8 or higher
- A Telegram bot token (You can get this by creating a bot on Telegram via [BotFather](https://t.me/BotFather))

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/MultiForwarderTGBot.git
    cd MultiForwarderTGBot
    ```

2. Create a virtual environment and activate it:
    ```sh
        python -m venv venv
        venv\Scripts\activate
        # source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Telegram bot token:
    ```env
    API_ID=your_telegram_api_id
    API_HASH=your_telegram_api_hash
    BOT_TOKEN=your_telegram_bot_tokeb
    MONGO_DB_URI=your_mongo_db_uri
    LOG_GROUP=your_telegram_log_group_id
    ADMIN_USERS_ID=admin_id admin_id admin_id
    FORCE_SUB_CHANNEL=your_must_join_telegram_channel_id
    ```

### Running the Bot

1. Start the bot:
    ```sh
    python -m multibot
    ```

2. Follow the instructions provided by the bot to configure the channels and destination.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

### License
This project is licensed under the MIT License.

For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/yourusername/MultiForwarderTGBot).

