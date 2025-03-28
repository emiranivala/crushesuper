import os
import datetime
from config import OWNER_ID
from Restriction import app, BOT_USERNAME
from pyrogram import filters
from Restriction.core.more_func import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



@app.on_message(filters.command("info"))
async def user_info(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    msg = await message.reply_text("Fetching...")
    lmao = await users_about(user_id, name)
    user = await _.get_users(user_id)
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Referral Link 🔗", url=f"https://telegram.dog/{BOT_USERNAME}?start=Referral_{user_id}")
        ], [
            InlineKeyboardButton("🧩 Referrals", callback_data="referrals_"),
            InlineKeyboardButton("☎️ Customers", callback_data="customers_")
        ]]
    )
    
    if user.photo:
        pic = await _.download_media(user.photo.big_file_id)      
        await message.reply_photo(pic, caption=lmao, reply_markup=buttons)
        await msg.delete()
        os.remove(pic)
    else:
        await msg.edit_text(lmao, reply_markup=buttons)

         



@app.on_message(filters.command("transfer"))
async def transfer(_, message):
    command_args = message.text.split(" ")[1:]
    reply = message.reply_to_message
    
    if reply:
        if len(command_args) < 1:
            return await message.reply_text(
                "Please specify the amount of coins to transfer. Example: `/transfer 500`."
            )
        user = reply.from_user.id
        coins = command_args[0]
    else:
        if len(command_args) < 2:
            return await message.reply_text(
                "Please provide the correct command. If you're not replying to a user's message, use `/transfer [user_id or @username] [coins]`."
            )
        user = command_args[0]
        coins = command_args[1]
    
    msg = await message.reply_text("Transferring...")
    text = await transfer_coin(_, message, user, coins)
    await msg.edit_text(text)




@app.on_message(filters.command("shop"))
async def shop(_, message):
    name = message.from_user.first_name
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("💲 Buy Coins", callback_data="buy_coins")
        ], [
            InlineKeyboardButton("☎️ Buy Premiums", callback_data="buy_premium")          
        ]]
    )
    await message.reply_photo(
        photo="static/crushe.jpg",
        caption=f"Hello {name}, welcome to the shop 🛍 ! You'll find everything you need related to bots here, all available for purchase.🛒",
        reply_markup=buttons
    )




@app.on_message(filters.command("rewards"))
async def rewards_(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name    
    can_collect, time_remaining = await collect_rewards(user_id)    
    if can_collect:
        await coin_rewards(user_id)
        await message.reply_text(f"Hello {name},\n\n🎉 Congrats! You've received 💰 20 coins for this week.")
    else:        
        await message.reply_text(f"Hey {name}, don't try to be over smart! 😏\n\nYou've already collected your rewards. Try again in {time_remaining}.")




@app.on_message(filters.command("refresh") & filters.user(OWNER_ID))
async def refresh_users(_, message):
    name = message.from_user.first_name
    msg = await message.reply_photo(
        photo="static/crushe.jpg", 
        caption="waitoo...")
    await premium_remover()
    await msg.edit_text(f"Heyoo {name},\n\nAll inactive premium users have been removed. Those whose premium time had expired have also been removed. 🍁")




@app.on_message(filters.command("add_customer"))
async def customers(_, message):
    try:
        await give_premium_customer(_, message)
    except Exception as e:
        print(f"**Error**: {e}")


@app.on_message(filters.command("remove_customer"))
async def remove_cust(_, message):
    try:
        await customer_remove(_, message)
    except Exception as e:
        await message.reply_text(f"Error: {e}")



@app.on_message(filters.command("remove_user") & filters.user(OWNER_ID))
async def remove_user(_, message):
    try:
        await shop_user_remove(_, message)
    except Exception as e:
        await message.reply_text(f"Error: {e}")






