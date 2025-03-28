from pyrogram import filters
from Restriction import app, BOT_USERNAME
from Restriction.core import script
from config import OWNER_ID
from pyrogram.errors import FloodWait
from Restriction.core.more_func import *
from Restriction.modules.settings import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton



# ------------------------------------------------------------------------------- #

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
         [[
               InlineKeyboardButton("ᴀᴅᴍɪɴs ᴘᴀɴɴᴇʟ", callback_data="admin_"),    
         ],[
               InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_"),    
         ]])


# ------------------- Back-Button ------------------- #

back_button  = InlineKeyboardMarkup([
	       [
                    InlineKeyboardButton("ɪɴsᴛʀᴜᴄᴛɪᴏɴs", url="https://t.me/Features_DB/5"), 
	            InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇs", url="https://t.me/Features_DB/4"),    
               ],[
                    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="home_"),                    
               ]])


# ------------------- Settings-Buttons ------------------- #

buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏜 ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumb_")                
            ],
	    [
                InlineKeyboardButton("📝 ᴄᴀᴘᴛɪᴏɴ", callback_data="caption_"),
		InlineKeyboardButton("🌐 ᴄʜᴀɴɴᴇʟ", callback_data="channel_")
            ],
	    [
                InlineKeyboardButton("📊 sᴇssɪᴏɴ", callback_data="session_"),
		InlineKeyboardButton("📇 ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="maintainer_")
            ]])


# ------------------- Thumb-Buttons ------------------- #

buttons2 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✚ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="set_thumb")              
            ],
            [
		InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_thumb"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_thumb"),
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ] 
        ])



# ------------------- Session-Buttons ------------------- #

buttons3 = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ sᴇᴛ sᴇssɪᴏɴ", callback_data="set_session")
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_session"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_session")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ]
        ])


# ------------------- Caption-Buttons ------------------- #

buttons4 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🖍️ʀᴇɴᴇᴡ ᴄᴀᴘᴛɪᴏɴ", callback_data="renew_"),
                InlineKeyboardButton("🖋️ʀᴇᴘʟᴀᴄᴇ ᴄᴀᴘᴛɪᴏɴ", callback_data="replace_")
            ],
            [
                InlineKeyboardButton("✚ ʀᴇᴍᴏᴠᴇ ᴡᴏʀᴅs", callback_data="words_"),
		InlineKeyboardButton("sᴏᴏɴ", callback_data="soon")
            ],    
	    [            
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_")		
            ]
        ])


# ------------------- Renew-Caption-Buttons ------------------- #

renew_button = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ʀᴇɴᴇᴡ ᴄᴀᴘᴛɪᴏɴ", callback_data="set_caption"),
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_caption"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_caption")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])


# ------------------- Replace-Caption-Buttons ------------------- #

replace_button = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ʀᴇᴘʟᴀᴄᴇ ᴄᴀᴘᴛɪᴏɴ", callback_data="re_caption"),
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="del_replace"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_replace")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])


# ------------------- Remove-Caption-Buttons ------------------- #

words_button = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ᴍᴏʀᴇ ᴡᴏʀᴅs", callback_data="add_words"),
            ],
            [          
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_words"),
		InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_words")                		
            ],
            [
		InlineKeyboardButton("📑 ᴅᴇʟᴇᴛᴇ ᴀʟʟ", callback_data="delall_words"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])

# ------------------- Channel-Buttons ------------------- #

buttons5 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✚ sᴇᴛ ᴄʜᴀɴɴᴇʟ", callback_data="set_chat")              
            ],
            [
		InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_chat"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_chat"),
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ] 
        ])



# ------------------- Callbacks-Buttons ------------------- #


@app.on_callback_query()
async def handle_callback(_, query):
    name = query.from_user.first_name
    user_id = query.from_user.id
    clicked = query.message.reply_to_message.from_user.id if query.message.reply_to_message else query.from_user.id

    if user_id == clicked:
        if query.data == "home_":
            return await query.message.edit_text(
                script.START_TXT.format(query.from_user.mention),
                reply_markup=buttons
            )

        elif query.data == "admin_":
            if user_id in OWNER_ID:
                return await query.message.edit_text(
                    script.ADMIN_TXT,
                    reply_markup=back_button
                )
            else:
                return await query.answer("This is not for you !!", show_alert=True)

        elif query.data == "help_":
            return await query.message.edit_text(
                script.HELP_TXT,
                reply_markup=back_button
            )

        elif query.data == "thumb_":
            return await query.message.edit_text(script.THUMBNAIL_TXT, reply_markup=buttons2)

        elif query.data == "caption_":
            return await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons4)

        elif query.data == "session_":
            return await query.message.edit_text(script.SESSION_TXT, reply_markup=buttons3)

        elif query.data == "channel_":
            return await query.message.edit_text(script.CHANNEL_TXT, reply_markup=buttons5)

        elif query.data == "back_":
            return await query.message.edit_text(script.SETTINGS_TXT, reply_markup=buttons1)

        elif query.data == "renew_":
            return await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=renew_button)

        elif query.data == "replace_":
            return await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=replace_button)

        elif query.data == "words_":
            return await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=words_button)

        elif query.data == "c_back":
            return await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons4)

        elif query.data == "set_thumb":
            return await add_thumb(query)

        elif query.data == "rm_thumb":
            return await remove_thumb(query)

        elif query.data == "views_thumb":
            return await view_thumb(query)

        elif query.data == "set_caption":
            return await add_caption(query)

        elif query.data == "rm_caption":
            return await delete_caption(query)

        elif query.data == "views_caption":
            return await see_caption(query)

        elif query.data == "re_caption":
            return await replace_func(query)

        elif query.data == "del_replace":
            return await rm_replace(query)

        elif query.data == "views_replace":
            return await see_replace(query)

        elif query.data == "views_session":
            return await view_session(query)

        elif query.data == "rm_session":
            return await delete_session(query)

        elif query.data == "set_session":
            return await add_session(query)

        elif query.data == "add_words":
            return await add_clearwords(query)

        elif query.data == "views_words":
            return await view_clearwords(query)

        elif query.data == "rm_words":
            return await remove_clearwords(query)

        elif query.data == "delall_words":
            return await deleteall_clearwords(query)

        elif query.data == "set_chat":
            return await add_channel(query)

        elif query.data == "views_chat":
            return await view_channel(query)

        elif query.data == "rm_chat":
            return await delete_channel(query)

        elif query.data == "buy_coins":
            button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Contact ☎️", url="https://t.me/She_who_remain")],
                    [InlineKeyboardButton("Back", callback_data="shop_")]
                ]
            )
            coins_price = """
💰 `750 Coins`  -  **200Rs**
💰 `1500 Coins` -  **400Rs**
💰 `2250 Coins` -  **600Rs**
💰 `3000 Coins` -  **750Rs**

You can contact via the given button to buy coins.
"""
            return await query.message.edit_text(coins_price, reply_markup=button)

        elif query.data == "buy_premium":
            button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("10 Days", callback_data="coins_350"),
                     InlineKeyboardButton("20 Days", callback_data="coins_500")],
                    [InlineKeyboardButton("1 Month", callback_data="coins_750"),
                     InlineKeyboardButton("Back", callback_data="shop_")]
                ]
            )
            premium_price = """
💰 `350 Coins`  -  **10 Days**
💰 `500 Coins` -  **20 Days**
💰 `750 Coins` -  **1 Month**

Click the provided button to purchase a premium plan according to your selected duration.
"""
            return await query.message.edit_text(premium_price, reply_markup=button)

        elif query.data == "shop_":
            return await query.message.edit_text(
                f"Hello {name}, welcome to the shop 🛍! You'll find everything you need related to bots here, all available for purchase.🛒",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("💲 Buy Coins", callback_data="buy_coins")],
                        [InlineKeyboardButton("☎️ Buy Premiums", callback_data="buy_premium")]
                    ]
                )
            )

        elif query.data.startswith("coins"):
            coins = int(query.data.split("_")[1])
            if coins == 350:
                duration = "10 day"
            elif coins == 500:
                duration = "20 day"
            elif coins == 750:
                duration = "1 month"
		    
            msg = await premium_store(_, user_id, name, coins, duration)
            return await query.message.edit_text(msg)

        elif query.data == "referrals_":
            await query.answer("waitooo", show_alert=True)
            msg = await referral_users(user_id, name)
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="info_")]
                ]
            )
            return await query.message.edit_text(msg, reply_markup=reply_markup)

        elif query.data == "customers_":
            await query.answer("waitooo", show_alert=True)
            msg = await customer_users(user_id, name)
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💲 Business", url="https://t.me/She_who_remain")],
                    [InlineKeyboardButton("Back", callback_data="info_")]
                ]
            )
            return await query.message.edit_text(msg, reply_markup=reply_markup)

        elif query.data == "info_":
            await query.answer("Fetching...", show_alert=True)
            lmao = await users_about(user_id, name)
            bs = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Referral Link 🔗", url=f"https://telegram.dog/{BOT_USERNAME}?start=Referral_{user_id}")],
                    [InlineKeyboardButton("🧩 Referrals", callback_data="referrals_"),
                     InlineKeyboardButton("☎️ Customers", callback_data="customers_")]
                ]
            )
            return await query.message.edit_text(lmao, reply_markup=bs)

        elif query.data == "maintainer_":
            return await query.answer("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ", show_alert=True)

        elif query.data == "close_data":
            try:
                await query.message.delete()
                return await query.message.reply_to_message.delete()
            except Exception as e:
                print(f"Error deleting messages: {e}")

    else:
        return await query.answer("This is not for you !!", show_alert=True)




	    
