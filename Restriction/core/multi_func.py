import base64
import random
import string
import aiohttp
import asyncio
from Restriction import BOT_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



api_keys = {
    "https://inshorturl.com/api?": "910fadcec0df945f8aa803869b497add2e9aa0ea",
    "https://modijiurl.com/api?": "af1e4b123035d25cfdec72c5378a5d91aac11207",
    "https://api.gplinks.com/api?": "3b2f7db4f2b84c96ee555458f7b92bee22e31e25", 
}



api_short = {}
short_verify = {}
verified_users = {}



def random_word(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_text(word_count, word_length):
    return ''.join(random_word(word_length) for _ in range(word_count))

def encode_base64(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


async def get_shortlink(link, api_url, api_key):
    if link.startswith("http://"):
        link = link.replace("http://", "https://")

    params = {'api': api_key, 'url': link}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json()
                if data["status"] == "success":
                    return data['shortenedUrl']
                else:
                    error_message = data.get('message', 'Unknown error occurred')
                    raise ValueError(f"Error: {error_message}")

    except aiohttp.ClientError as e:
        raise ValueError(f"HTTP request error: {e}")

    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")




async def api_func(user_id):    
    api_urls = list(api_keys.keys())    
    if user_id in verified_users:
        if user_id in api_short:
            current_api_index = api_short[user_id]
            next_api_index = (current_api_index + 1) % len(api_urls)
            api_short[user_id] = next_api_index
            return api_urls[next_api_index], api_keys[api_urls[next_api_index]]
        else:
            api_short[user_id] = 0
            return api_urls[0], api_keys[api_urls[0]]
    else:
        if user_id in api_short:
            return api_urls[api_short[user_id]], api_keys[api_urls[api_short[user_id]]]
        else:
            api_short[user_id] = 0
            return api_urls[0], api_keys[api_urls[0]]



async def verification_sender(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    random_text = generate_random_text(7, 5)
    encoded_text = encode_base64(random_text)
    short_verify[user_id] = encoded_text
    encode_url = f"https://telegram.dog/{BOT_USERNAME}?start=Verify_{encoded_text}"
    api_url, api_key = await api_func(user_id)
    url = await get_shortlink(encode_url, api_url, api_key)
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("CLICK", url=url)]      
    ])
    await message.reply_text(f"<b><i>Heyoo {name}, please complete the shortener verification 🔒 to access the files through the bot 📁. The verification is valid for 3 hours ⏰.</i></b>",
                             reply_markup=button)



async def verification_accepter(_, message):
    parts = message.text.split("_")
    token = parts[1]
    user_id = message.from_user.id
    name = message.from_user.first_name
    if user_id in short_verify and short_verify[user_id] == token:
        if user_id not in verified_users:
            verified_users[user_id] = "Verified"
            asyncio.create_task(clear_verify(message, delay=21600))
            await message.reply_text(f"Hello {name}, your account has been successfully approved ✅")
            api_key = await api_func(user_id)
            print(f"API Key for User {name}: {api_key}")
            return
        else:
            await message.reply_text(f"Hello {name}, your account has already been successfully approved ✅")
    else:
        await message.reply_text("Don't act too smart 😏")



async def clear_verify(message, delay):
    user_id = message.from_user.id
    name = message.from_user.first_name
    await asyncio.sleep(delay)
    verified_users.pop(user_id, None)
    short_verify.pop(user_id, None)
    print(f"Hey {name}, Your Shortener time is over")



