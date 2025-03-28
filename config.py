from os import getenv


API_ID = int(getenv("API_ID", "22642292"))
API_HASH = getenv("API_HASH", "4502d35191a2fcb02c8467f54789f0ea")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "922270982 7446465090").split()))
MONGO_DB = getenv("MONGO_DB", "")

CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002304203111"))
PREMIUM_LOGS = int(getenv("PREMIUM_LOGS", "-1002230414810"))
