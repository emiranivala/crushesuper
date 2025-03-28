import pytz
import asyncio
import datetime
from Restriction import app
from Restriction.core.mongo.shopesdb import *
from config import OWNER_ID as owner, PREMIUM_LOGS
from Restriction.core.func import get_seconds
from Restriction.core.mongo import plansdb as plans_db
from Restriction.core.mongo.plansdb import premium_users



async def reffer_verified(_, message, reffer_id):
    try:
        try:
            user = await _.get_users(reffer_id)
        except:
            return await message.reply_text("Don't act too smart 😏")
            
        user_id = message.from_user.id
        name = message.from_user.first_name
        user_data = await get_user_data(reffer_id)
        lmao_data = await get_user_data(user_id)
        
        if user_id not in user_data.get("reffers_id", []) and reffer_id not in lmao_data.get("reffers_id", []):
            await user_store(user_id, 5)
            await message.reply_text(f"Hello {name}, Congrats 🎉 You Got 5 Coins.")
            await user_store(reffer_id, 10)
            await add_reffers(reffer_id, user_id)
            
            try:          
                await _.send_message(
                    chat_id=reffer_id,
                    text=f"Hello {user.first_name}, Congrats 🎉 you received 10 coins. {name} used your referral link."
                )
            except Exception as e:
                print(f"Failed to send message to {user.first_name}: {e}")
        else:
            await message.reply_text("Don't act too smart 😏")
    except Exception as e:
        await message.reply_text(f"Something went wrong !!\n\n**Error**: {e}")
        



async def users_about(user_id, name):
    users_data = user_data = await get_user_data(user_id)
    users_info = f"""
🍁 **Name** : `{name}`
👀 **Users ID**: `{user_id}`
💰 **Coins**: `{users_data['coins']}`
    
👒 **Refferals**: `{len(users_data['reffers_id'])}`
📝 **Customers**: `{len(users_data['customers'])}`
    """
    return users_info
    



async def transfer_coin(_, message, user, coins):
    user_id = message.from_user.id
    name = message.from_user.first_name
    transfee = await _.get_users(user)
    user_data = await get_user_data(user_id)
    coins = int(coins)
    
    if user_data["coins"] >= coins or user_id in owner:
        if user_id in owner:
            await user_store(transfee.id, coins)
        else:
            await user_store(user_id, -coins)
            await user_store(transfee.id, coins)
        
        msg = f"Hello {name},\n\nYour 💰 {coins} coins have been successfully transferred to {transfee.first_name}. 🎉"
        return msg
    else:
        msg = "Oops! 😕 It looks like you don't have enough 💰 balance."
        return msg





async def premium_store(_, user_id, name, coins, duration):
    seconds = await get_seconds(duration)
    user_data = await get_user_data(user_id)
    
    if user_data["coins"] >= coins:
        await user_store(user_id, -coins)
        
        if seconds > 0:
            expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
            await plans_db.add_premium(user_id, expiry_time)
            
            msg = f"Hello {name},\n\nCongratulations! 🎉 You've received a {duration} premium subscription. Enjoy! 😄"
            
            data = await plans_db.check_premium(user_id)
            expiry = data.get("expire_date")
            
            if expiry:
                expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ **ᴇxᴘɪʀʏ ᴛɪᴍᴇ** : %I:%M:%S %p")
                current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ **ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ** : %I:%M:%S %p")                
                await _.send_message(PREMIUM_LOGS, text=f"**❰ ʀᴇsᴛʀɪᴄᴛɪᴏɴ ʙᴏᴛ ❱**\n\n👤 **ᴜꜱᴇʀ** : {name}\n⚡ **ᴜꜱᴇʀ ɪᴅ** : <code>{user_id}</code>\n⏰ **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ** : <code>{duration}</code>\n\n⏳ **ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ** : {current_time}\n\n⌛️ **ᴇxᴘɪʀʏ ᴅᴀᴛᴇ** : {expiry_str_in_ist}", disable_web_page_preview=True)           
            return msg
                    
    else:      
        msg = "Oops! 😕 It looks like you don't have enough 💰 balance."
        return msg





async def premium_remover():
    all_users = await plans_db.premium_users()
    for user_id in all_users:
        try:
            user = await app.get_users(user_id)
            chk_time = await plans_db.check_premium(user_id)
        
            if chk_time and chk_time.get("expire_date"):
                expiry_date = chk_time["expire_date"]
                        
                if expiry_date <= datetime.datetime.now():
                    name = user.first_name
                    await plans_db.remove_premium(user_id)
                    await app.send_message(user_id, text=f"Hello {name}, your premium subscription has expired.")
                    print(f"{name}, your premium subscription has expired.")
            
                else:
                    name = user.first_name
                    current_time = datetime.datetime.now()
                    time_left = expiry_date - current_time
                    
                    days = time_left.days
                    hours, remainder = divmod(time_left.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    
                    if days > 0:
                        remaining_time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                    elif hours > 0:
                        remaining_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
                    elif minutes > 0:
                        remaining_time = f"{minutes} minutes, {seconds} seconds"
                    else:
                        remaining_time = f"{seconds} seconds"
        
                    print(f"{name} : Remaining Time : {remaining_time}")
        except:
            await plans_db.remove_premium(user_id)
            print(f"unknown users captured : {user_id} removed")




async def collect_rewards(user_id):
    user_data = await get_user_data(user_id)
    collection_time = user_data.get('weekly_rewards')
    
    if collection_time is None:
        return True, 0
    
    last_collection_time = datetime.datetime.fromtimestamp(collection_time)
    current_time = datetime.datetime.now()
    time_since_last_collection = current_time - last_collection_time
    seconds_in_a_week = 7 * 24 * 60 * 60
    
    can_collect = time_since_last_collection.total_seconds() >= seconds_in_a_week
    time_until_next_collection = max(0, seconds_in_a_week - time_since_last_collection.total_seconds())
    
    days, remainder = divmod(time_until_next_collection, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        remaining_time = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    elif hours > 0:
        remaining_time = f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    elif minutes > 0:
        remaining_time = f"{int(minutes)} minutes, {int(seconds)} seconds"
    else:
        remaining_time = f"{int(seconds)} seconds"
            
    return can_collect, remaining_time


async def coin_rewards(user_id):
    await user_store(user_id, 20)
    await weekly_rewards(user_id, datetime.datetime.now().timestamp())
    print(f"This user id {user_id} : Received 💰")




async def referral_users(user_id, name):
    user_data = await get_user_data(user_id)
    referral_users = user_data.get("reffers_id")    
    if referral_users == False:
        return "You don't have any referral users 😌"

    reff_msg = f"Hello {name}, these are your referral users.\n\n"
    for um in referral_users:
        try:
            user = await app.get_users(um)
            reff_msg += f"<pre>⬤ {user.first_name} - {um}</pre>\n"
        except:
            reff_msg += f"<pre>⬤ unknown - not defined</pre>\n"
            
    return reff_msg





async def customer_users(user_id, name):
    user_data = await get_user_data(user_id)
    customer_users = user_data.get("customers")    
    if customer_users == False:
        return "You don't have any customer users 😌"

    msg = f"Hello {name}, these are your premium customer users.\n\n"
    for customer_id in customer_users:
        cid = customer_id["customer_id"]
        customer_name = customer_id["customer_name"]
        
        customer_date = customer_id["customer_time"]
        customer_time = customer_date.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
        
        expiry_date = customer_id["customer_expiry"]
        customer_expiry = expiry_date.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")                    
        current_time = datetime.datetime.now()
        time_left = expiry_date - current_time
        
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            remaining_time = f"{days} ᴅᴀʏs, {hours} ʜᴏᴜʀs, {minutes} ᴍɪɴᴜᴛᴇs, {seconds} sᴇᴄᴏɴᴅs"
        elif hours > 0:
            remaining_time = f"{hours} ʜᴏᴜʀs, {minutes} ᴍɪɴᴜᴛᴇs, {seconds} sᴇᴄᴏɴᴅs"
        elif minutes > 0:
            remaining_time = f"{minutes} ᴍɪɴᴜᴛᴇs, {seconds} sᴇᴄᴏɴᴅs"
        else:
            remaining_time = f"{seconds} sᴇᴄᴏɴᴅs"
        
        try:            
            user = await app.get_users(cid)
            msg += f"""<pre>
👤 ɴᴀᴍᴇ : {user.first_name}
🧩 ᴜsᴇʀ ɪᴅ : {cid}
🗓 ᴅᴀᴛᴇ : {customer_time}
⏱ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {customer_expiry}
⏳ ᴛɪᴍᴇ ʟᴇғᴛ : {remaining_time}
</pre>\n"""
        except:
            msg += f"""<pre>
👤 ɴᴀᴍᴇ : {customer_name} - Deleted Account
🧩 ᴜsᴇʀ ɪᴅ : {cid}
🗓 ᴅᴀᴛᴇ : {customer_time}
⏱ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {customer_expiry} 
⏳ ᴛɪᴍᴇ ʟᴇғᴛ : {remaining_time}
</pre>\n"""
            
    return msg





async def calculate_coins(total_coins, total_days, input_days):
    coins_per_day = total_coins / total_days
    calculated_coins = coins_per_day * input_days
    if input_days > 15:
        calculated_coins -= 50

    return max(int(calculated_coins), 0)



async def give_premium_customer(_, message):
    reply = message.reply_to_message
    user_id = message.from_user.id
    name = message.from_user.first_name
    premiums = await premium_users()
    msg = await message.reply_text("Processing...")

    if user_id not in premiums:
        await msg.edit_text("You are not a premium user, only premium users can access this command.")
        return
    
    if reply:
        c_user = reply.from_user.id
        input_days = int(message.command[1])
        time = message.command[1] + " " + message.command[2]
        
        if user_id == c_user:
            await msg.edit_text("You cannot assign premium to yourself.")
            return
        
    elif len(message.command) == 4:
        c_user = int(message.command[1])
        input_days = int(message.command[2])
        time = message.command[2] + " " + message.command[3]
        
        if user_id == c_user:
            await msg.edit_text("You cannot assign premium to yourself.")
            return
    else:
        return await msg.edit_text("Usage: /add_customer <user_id> <duration> <unit> or reply to a user with '/add_customer <duration> <unit>'")

    user_data = await get_user_data(user_id)
    time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = time_zone.strftime("%d-%m-%Y\n⏱️ **ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ**: %I:%M:%S %p") 

    customer = await _.get_users(c_user)
    coins = await calculate_coins(350, 10, input_days)
    
    if user_data["coins"] >= coins:
        await user_store(user_id, -coins)
        
        seconds = await get_seconds(time)
        if 86399 > seconds:
            await msg.edit_text("Don't give a duration of less than 1 day, it's not valid.")
            return 
            
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            await plans_db.add_premium(c_user, expiry_time)
            
            data = await plans_db.check_premium(c_user)
            expiry = data.get("expire_date")
            expiry_date = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ **ᴇxᴘɪʀʏ ᴛɪᴍᴇ** : %I:%M:%S %p")
            
            await add_customer(user_id, customer.id, customer.first_name, datetime.datetime.now(), expiry)
            
            await msg.edit_text(f"Hello {name}, Your Customer's Premium has been successfully added ✅\n\n👤 Name : {customer.first_name}\n👀 User ID: <code>{c_user}</code>")
            
            await _.send_message(
                chat_id=c_user,
                text=f"Hey {customer.first_name},\nThank you for purchasing premium. Enjoy! 🎉✨\n\n⏰ **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ** : <code>{time}</code>\n⏳ **ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ** : {current_time}\n⌛️ **ᴇxᴘɪʀʏ ᴅᴀᴛᴇ** {expiry_date}",
                disable_web_page_preview=True
            )            
            await _.send_message(PREMIUM_LOGS, text=f"**❰ ʀᴇsᴛʀɪᴄᴛɪᴏɴ ʙᴏᴛ ❱**\n\n👤 **ᴜꜱᴇʀ** : {customer.first_name}\n⚡ **ᴜꜱᴇʀ ɪᴅ** : <code>{c_user}</code>\n⏰ **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ** : <code>{time}</code>\n\n⏳ **ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ** : {current_time}\n\n⌛️ **ᴇxᴘɪʀʏ ᴅᴀᴛᴇ** : {expiry_date}", disable_web_page_preview=True)           
            
        else:
            await msg.edit_text("Invalid time format. Please use '1 day', '1 hour', '1 min', '1 month', or '1 year'.")
    else:
        await msg.edit_text("Oops! 😕 It looks like you don't have enough balance.")




async def shop_user_remove(_, message):
    name = message.from_user.first_name   
    reply = message.reply_to_message 

    if reply:
        user = reply.from_user        
    else:
        command_args = message.text.split(" ", 2)[1:]
        if len(command_args) < 1:
            return await message.reply_text(f"Hello {name}, please reply to a user's message or provide a user ID.\nUsage: `/remove_user user_id`")
            
        s_user_id = command_args[0]
        try:
            user = await _.get_users(s_user_id)
        except Exception as e:
            return await message.reply_text(f"Sorry {name}, there was an error: {str(e)}. Please make sure the user ID is correct.")
    
    result = await remove_shop_user(user.id)
    
    if result:
        await message.reply_text(f"Hello {name},\nThe shop user has been successfully removed.\n\n👤 **Name**: {user.first_name}\n👀 **User ID**: {user.id}")
    else:
        await message.reply_text(f"Are you sure? It seems like this user doesn't exist in the shop's database.")




async def customer_remove(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    reply = message.reply_to_message
    
    if reply:
        user = reply.from_user
    else:
        command_args = message.text.split(" ", 2)[1:]
        if len(command_args) < 1:
            return await message.reply_text(f"Hello {name}, please reply to a user's message or provide a user ID.\nUsage: `/remove_customer user_id`")
        
        customer_id = command_args[0]
        try:
            user = await _.get_users(customer_id)
        except Exception as e:
            return await message.reply_text(f"Sorry {name}, there was an error: {str(e)}. Please make sure the user ID is correct.")
    
    result = await remove_customer(user_id, user.id)
    if result:
        await plans_db.remove_premium(user_id)
        await message.reply_text(f"Hello {name}, your customer's account has been successfully removed.\n\n👤 **Name**: {user.first_name}\n👀 **User ID**: `{user.id}`")        
    else:
        await message.reply_text("Oops! It seems this user doesn't exist in your customer's database.")





