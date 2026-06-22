from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import os
import asyncio

from utils.misc import modules_help, prefix

TXT_FILE = "database/oneword.txt"
active_tasks = {}

def load_txt_list():
    if not os.path.exists(TXT_FILE):
        os.makedirs(os.path.dirname(TXT_FILE), exist_ok=True)
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            pass
    
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

@Client.on_message(filters.command("ow", prefix) & filters.me)
async def activate_loop(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id in active_tasks:
        await message.delete()
        return

    text_list = load_txt_list()
    if not text_list:
        await message.delete()
        return
        
    await message.delete()
    reply_to_id = message.reply_to_message.id if message.reply_to_message else None
    
    active_tasks[chat_id] = True

    for item in text_list:
        if chat_id not in active_tasks:
            break
            
        try:
            if reply_to_id:
                await client.send_message(chat_id, item, reply_to_message_id=reply_to_id)
            else:
                await client.send_message(chat_id, item)
            
            # Extreme Fast Speed
            await asyncio.sleep(0.1)
            
        except FloodWait as e:
            # FloodWait aane par bot bina ruke utne seconds wait karke khud aage badhega
            await asyncio.sleep(e.value + 1)
            
        except Exception:
            await asyncio.sleep(0.1)

    active_tasks.pop(chat_id, None)

@Client.on_message(filters.command("owstop", prefix) & filters.me)
async def stop_loop(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_tasks:
        active_tasks.pop(chat_id, None)
    
    await message.delete()

modules_help["oneword"] = {
    "ow": "Sequence",
    "owstop": "Stop"
}
