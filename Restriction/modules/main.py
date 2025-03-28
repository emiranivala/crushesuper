import time
import asyncio
from pyrogram import filters, Client
from Restriction import app
from config import API_ID, API_HASH, OWNER_ID as owner
from Restriction.core.get_func import get_msg
from Restriction.core.func import *
from Restriction.core.multi_func import *
from Restriction.core.mongo.plansdb import premium_users
from Restriction.core.mongo import settingsdb as db
from pyrogram.errors import FloodWait
from Restriction.core.func import chk_user


spam_db = []

@app.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def single_link(_, message):
    user_id = message.from_user.id
    join = await subscribe(_, message)
    if join == 1:
        return

    user = await premium_users()
    if user_id not in user and user_id not in verified_users:
        await verification_sender(_, message)
        return

    link = get_link(message.text)
    if user_id in spam_db:
        return await message.reply_text("<b><i>Please wait; the video is currently being downloaded. Avoid spamming.</i></b>")
    spam_db.append(user_id)

    try:
        msg = await message.reply_text("<b><i>Processing By Crushe...</i></b>")
        data = await db.get_data(user_id)

        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()
            except:
                spam_db.remove(user_id)
                return await msg.edit_text("<b><i>Please generate a new session.</i></b>")
        else:
            spam_db.remove(user_id)
            await msg.edit_text("<b><i>Please generate a session first.</i></b>")

        if 't.me/+' in link:
            lol = await userbot_join(userbot, link)
            await msg.edit_text(lol)
            spam_db.remove(user_id)
            return

        if 't.me/' in link:
            asyncio.create_task(get_msg(userbot, user_id, msg.id, link, msg))
            spam_db.remove(user_id)


    except FloodWait as fw:
        spam_db.remove(user_id)
        await msg.edit_text(f"<b><i>Try again after {fw.x} seconds due to Telegram flood wait.</i></b>")
    except Exception as e:
        spam_db.remove(user_id)
        await msg.edit_text(f"<b><i>Error: {str(e)}</i></b>")



users_loop = {}

async def process_and_upload_link(userbot, user_id, msg_id, link, msg):
    try:
        await get_msg(userbot, user_id, msg_id, link, msg)
        await asyncio.sleep(2.5)
    finally:
        pass



@app.on_message(filters.command("batch") & filters.private)
async def batch_link(_, message):
    user_id = message.from_user.id
    join = await subscribe(_, message)
    if join == 1:
        return

    lol = await chk_user(message, user_id)
    if lol == 1:
        return

    if user_id in spam_db:
        return await message.reply_text("<b><i>Please wait; the video is currently being downloaded. Avoid spamming.</i></b>")
    spam_db.append(user_id)

    start = await app.ask(message.chat.id, text="<b><i>Please send the start link.</i></b>")
    start_id = start.text
    s = start_id.split("/")[-1]

    last = await app.ask(message.chat.id, text="<b><i>Please send the end link.</i></b>")
    last_id = last.text
    l = last_id.split("/")[-1]

    try:
        data = await db.get_data(user_id)

        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()
            except Exception as e:
                spam_db.remove(user_id)
                return await app.send_message(message.chat.id, f"<b><i>Error starting userbot: {str(e)}. Please generate a new session.</i></b>")
        else:
            spam_db.remove(user_id)
            return await app.send_message(message.chat.id, "<b><i>Please generate a session first.</i></b>")

        users_loop[user_id] = True

        for i in range(int(s), int(l) + 1):
            if user_id in users_loop and users_loop[user_id]:
                msg = await message.reply_text("<b><i>Processing By Crushe...</i></b>")
                try:
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)

                    await process_and_upload_link(userbot, user_id, msg.id, link, msg)

                except Exception as e:
                    await msg.edit_text(f"<b><i>Error processing link {url}: {e}</i></b>")
                    continue
            else:
                await app.send_message(message.chat.id, "<b><i>Batch process has been stopped.</i></b>")
                break
        else:
            users_loop[user_id] = False
            await message.reply_text("✅ Successfully downloaded all files by Crushe.")
            spam_db.remove(user_id)

    except FloodWait as fw:
        await app.send_message(message.chat.id, f"<b><i>Try again after {fw.x} seconds due to Telegram flood wait.</i></b>")
    except Exception as e:
        spam_db.remove(user_id)
        await app.send_message(message.chat.id, f"<b><i>Error: {str(e)}</i></b>")




@app.on_message(filters.command("fbatch") & filters.private)
async def fbatch_link(_, message):
    user_id = message.from_user.id
    join = await subscribe(_, message)
    if join == 1:
        return

    user = await premium_users()
    if user_id not in user and user_id not in verified_users:
        await verification_sender(_, message)
        return

    if user_id in spam_db:
        return await message.reply_text("<b><i>Please wait; the video is currently being downloaded. Avoid spamming.</i></b>")
    
    spam_db.append(user_id)

    start = await app.ask(message.chat.id, text="<b><i>Please send the start link.</i></b>")
    start_id = start.text
    s = int(start_id.split("/")[-1]) 

    try:
        data = await db.get_data(user_id)

        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()
            except:
                spam_db.remove(user_id)
                return await app.send_message(message.chat.id, "<b><i>Please generate a new session.</i></b>")
        else:
            spam_db.remove(user_id)
            return await app.send_message(message.chat.id, "<b><i>Please generate a session first.</i></b>")

        users_loop[user_id] = True

        for i in range(s, s + 21): 
            await asyncio.sleep(1.5)
            if user_id in users_loop and users_loop[user_id]:
                msg = await message.reply_text("<b><i>Processing By Crushe...</i></b>")
                try:
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)
                    
                    await process_and_upload_link(userbot, user_id, msg.id, link, msg)
                except Exception as e:
                    print(f"Error processing link {url}: {e}")
                    continue
            else:
                await app.send_message(message.chat.id, "<b><i>Batch process has been stopped.</i></b>")
                spam_db.remove(user_id)
                break
        else:
            users_loop[user_id] = False
            await message.reply_text("✅ Successfully downloaded all files by Crushe.")
            spam_db.remove(user_id)

    except FloodWait as fw:
        await app.send_message(message.chat.id, f"<b><i>Try again after {fw.x} seconds due to Telegram flood wait.</i></b>")
    except Exception as e:
        spam_db.remove(user_id)
        await app.send_message(message.chat.id, f"<b><i>Error: {str(e)}</i></b>")




@app.on_message(filters.command("stop") & filters.private)
async def stop_batch(_, message):
    user_id = message.from_user.id
    if user_id in users_loop and users_loop[user_id]:
        spam_db.remove(user_id)
        users_loop[user_id] = False
        await app.send_message(message.chat.id, "<b><i>Batch processing stopped.</i></b>")
    else:
        await app.send_message(message.chat.id, "<b><i>No active batch to stop.</i></b>")





