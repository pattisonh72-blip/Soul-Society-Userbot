import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
# Dragon Userbot ke standard imports jo aapne screenshot mein dikhaye
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

TXT_FILE = "database/oneword.txt"
active_tasks = set()

def load_txt_list():
    if not os.path.exists(TXT_FILE):
        os.makedirs(os.path.dirname(TXT_FILE), exist_ok=True)
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            pass
    
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

@Client.on_message(filters.command("ow", prefix) & filters.me)
async def activate_loop(client: Client, message: Message):
    text_list = load_txt_list()
    if not text_list:
        await message.delete()
        return
        
    task_id = asyncio.current_task()
    active_tasks.add(task_id)
    
    await message.delete()
    reply_to_id = message.reply_to_message.id if message.reply_to_message else None

    for item in text_list:
        if task_id not in active_tasks:
            break
        try:
            if reply_to_id:
                await client.send_message(message.chat.id, item, reply_to_message_id=reply_to_id)
            else:
                await client.send_message(message.chat.id, item)
            
            await asyncio.sleep(0.15)
            
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except Exception as e:
            # Agar koi unexpected error aaye toh console log mein dikhega
            print(format_exc(e))

    if task_id in active_tasks:
        active_tasks.remove(task_id)

@Client.on_message(filters.command("owstop", prefix) & filters.me)
async def stop_loop(client: Client, message: Message):
    global active_tasks
    active_tasks.clear() 
    await message.delete()

# Help dictionary jismein khali ya minimal commands hain jaisa aapko chahiye tha
modules_help["oneword"] = {
    "ow": "Sequence",
    "owstop": "Stop"
}
            if reply_to_id:
                await client.send_message(message.chat.id, item, reply_to_message_id=reply_to_id)
            else:
                await client.send_message(message.chat.id, item)
            
            await asyncio.sleep(0.15)
            
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except Exception:
            pass

    if task_id in active_tasks:
        active_tasks.remove(task_id)

@Client.on_message(filters.command("owstop", prefix) & filters.me)
async def stop_loop(client, message):
    global active_tasks
    active_tasks.clear() 
    await message.delete()

# Dragon Userbot ka help menu structure
modules_help["oneword"] = {
    "ow": "Run sequence",
    "owstop": "Stop sequence"
}
