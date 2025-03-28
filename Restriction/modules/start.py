from pyrogram import filters
from Restriction import app
from Restriction.core import script
from Restriction.core.func import subscribe
from Restriction.modules.callbacks import buttons
from Restriction.core.multi_func import *
from Restriction.core.more_func import reffer_verified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery




@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return
        
    if message.text.startswith("/start Verify"):
        await verification_accepter(_, message)
        return 
        
    if message.text.startswith("/start Referral"):
        reffer_id = message.text.split("_")[1]
        await reffer_verified(_, message, int(reffer_id))
        return 
    else:
        await message.reply_photo(
            photo="static/crushe.jpg",
            caption=script.START_TXT.format(message.from_user.first_name),
            reply_markup=buttons
        )





