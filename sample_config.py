import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
LOG_GROUP = int(os.environ.get("LOG_GROUP"))
ADMIN_USERS_ID = list(map(int, os.environ.get("ADMIN_USERS_ID").split()))
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL"))
