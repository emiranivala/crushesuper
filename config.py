from os import getenv


API_ID = int(getenv("API_ID", "24210243"))
API_HASH = getenv("API_HASH", "509031fb3790b968e489f71d591ebce5")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "922270982 7446465090").split()))
MONGO_DB = getenv("MONGO_DB", "")

CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002294535138"))
PREMIUM_LOGS = int(getenv("PREMIUM_LOGS", "-1002458919549"))


