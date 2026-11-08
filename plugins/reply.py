import os
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import db 

# Database Collection
replies = db["auto_replies"]


OWNER_ID_STR = os.environ.get("OWNER_ID", "0")
OWNER_IDS = [int(i.strip()) for i in OWNER_ID_STR.split(",") if i.strip().isdigit()]


reactions_list = ["👎", "👍", "👌", "🙏", "🤌", "🫰", "💘", "🍓", "💯", "🤣", "😭","❤","❌"]


BOT_MENTION_REPLY = "**မင်္ဂလာပါ ခင်ဗျာ! ကျွန်တော့်က AutoReply ဖြစ်ပါတယ်**"

@Client.on_message(filters.group & ~filters.bot)
async def auto_learn_and_reply(client: Client, message: Message):
    
    
    bot_username = (await client.get_me()).username
    is_mentioned = False
    
    if message.mentioned:
        is_mentioned = True
    elif message.reply_to_message and message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id == (await client.get_me()).id:
            is_mentioned = True

    
    if is_mentioned:
        try:
            random_emoji = random.choice(reactions_list)
            await client.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji=random_emoji
            )
        except Exception:
            pass
            
        return await message.reply_text(BOT_MENTION_REPLY)

    
    if message.reply_to_message:
        reply_to = message.reply_to_message
        
        trigger = None
        trigger_type = None
        
        if reply_to.text:
            trigger = reply_to.text.lower().strip()
            trigger_type = "text"
        elif reply_to.sticker:
            trigger = reply_to.sticker.file_unique_id
            trigger_type = "sticker"

        reply_data = None
        reply_type = None
        
        if message.text:
            reply_data = message.text
            reply_type = "text"
        elif message.sticker:
            reply_data = message.sticker.file_id
            reply_type = "sticker"

        if trigger and reply_data:
            exists = await replies.find_one({"trigger": trigger})
            if not exists:
                await replies.insert_one({
                    "trigger": trigger,
                    "trigger_type": trigger_type,
                    "reply": reply_data,
                    "reply_type": reply_type
                })

    
    else:
        current_trigger = None
        if message.text:
            current_trigger = message.text.lower().strip()
        elif message.sticker:
            current_trigger = message.sticker.file_unique_id

        if current_trigger:
            found = await replies.find_one({"trigger": current_trigger})
            if found:
                try:
                    random_emoji = random.choice(reactions_list)
                    await client.send_reaction(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        emoji=random_emoji
                    )
                except Exception as e:
                    print(f"Reaction Error: {e}")

                if found["reply_type"] == "text":
                    await message.reply_text(found["reply"])
                else:
                    await message.reply_sticker(found["reply"])


@Client.on_message(filters.command("del"))
async def delete_reply(client: Client, message: Message):
    if not message.from_user or message.from_user.id not in OWNER_IDS:
        return 

    if not message.reply_to_message:
        return await message.reply_text("❌ ဖျက်ချင်တဲ့ အမေးစာကို Reply ပြန်ပြီး `/del` လို့ ရိုက်ပါ။")

    reply_to = message.reply_to_message
    trigger_to_del = None
    
    if reply_to.text:
        trigger_to_del = reply_to.text.lower().strip()
    elif reply_to.sticker:
        trigger_to_del = reply_to.sticker.file_unique_id

    if trigger_to_del:
        result = await replies.delete_many({"trigger": trigger_to_del})
        if result.deleted_count > 0:
            await message.reply_text(f"🗑️ အမေးစာ '{trigger_to_del}' အတွက် အဖြေကို Global Database ထဲက ဖျက်လိုက်ပါပြီ။")
        else:
            await message.reply_text("❌ ဒီစာသားအတွက် မှတ်ထားတဲ့ အဖြေမရှိပါဘူး။")
