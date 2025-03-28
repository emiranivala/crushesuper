import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN


# ---------------------------------------------------------------- #

loop = asyncio.get_event_loop()


app = Client(
    ":RestrictBot:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=32  
)



# ----------------------------Bot-Info---------------------------- #

async def bot_info():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    app.set_parse_mode(ParseMode.DEFAULT)
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(bot_info())

# ---------------------------------------------------------------- #



