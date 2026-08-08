# Copyright (c) 2026 khithlainhtet
# PANDAMusic / Telegram Bot Plugin

from pyrogram import Client, filters
from pyrogram.types import Message


ANTILINK_STATUS = {}


import re

def has_link(text: str) -> bool:
    if not text:
        return False
    # URL များနှင့် t.me လင့်ခ်များကို ရှာဖွေရန် Regex
    url_pattern = r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.dog/\S+)"
    return bool(re.search(url_pattern, text))

# -------------------------------------------------------------------------
# 
# -------------------------------------------------------------------------
@Client.on_message(filters.command(["antilink"]) & filters.group)
async def toggle_antilink(client: Client, message: Message):
    chat_id = message.chat.id
    
    
    user = await client.get_chat_member(chat_id, message.from_user.id)
    if user.status not in ["creator", "administrator"]:
        return await message.reply_text("❌ ဒီ Command ကို Admin တွေမှသာ အသုံးပြုနိုင်ပါတယ်။")

    # Command နောက်က argument ကို စစ်ခြင်း (ဥပမာ: /antilink on သို့မဟုတ် /antilink off)
    if len(message.command) < 2:
        current = ANTILINK_STATUS.get(chat_id, False)
        status_text = "ဖွင့်ထားသည် 🟢" if current else "ပိတ်ထားသည် 🔴"
        return await message.reply_text(f"ℹ️ လက်ရှိ Anti-Link အခြေအနေ: **{status_text}**\n\nသုံးစွဲရန်: `/antilink on` သို့မဟုတ် `/antilink off`")

    arg = message.command[1].lower()
    if arg == "on":
        ANTILINK_STATUS[chat_id] = True
        await message.reply_text("✅ ဤဂရုအတွက် **Anti-Link** စနစ်ကို  **ဖွင့်လိုက်ပါပြီ**။")
    elif arg == "off":
        ANTILINK_STATUS[chat_id] = False
        await message.reply_text("❌ ဤဂရုအတွက် **Anti-Link** စနစ်ကို **ပိတ်လိုက်ပါပြီ**။")
    else:
        await message.reply_text("⚠️ မှားယွင်းနေပါသည်။ `/antilink on` (သို့) `/antilink off` ဟု ရေးပါ။")

# -------------------------------------------------------------------------
# 
# -------------------------------------------------------------------------
@Client.on_message(filters.group & ~filters.service, group=6)
async def check_links(client: Client, message: Message):
    chat_id = message.chat.id
    
    # 
    if not ANTILINK_STATUS.get(chat_id, False):
        return

    # 
    if message.from_user:
        try:
            member = await client.get_chat_member(chat_id, message.from_user.id)
            if member.status in ["creator", "administrator"]:
                return
        except Exception:
            pass

    #
    text_to_check = message.text or message.caption or ""
    
    if has_link(text_to_check):
        try:
            #
            await message.delete()
            
            #
            warning_msg = await message.reply_text(
                f"⚠️ **{message.from_user.mention}**၊ ဤဂရုအတွင်း လင့်ခ် (Links) တင်ခွင့်မပြုပါ။ ကျေးဇူးပြု၍ လင့်ခ်များ မတင်ပါနဲ့။"
            )
            
            # လိုအပ်ပါက သတိပေးချက်ကို ၅ စက္ကန့်အကြာ ပြန်ဖျက်ရန်
             import asyncio
             await asyncio.sleep(5)
             await warning_msg.delete()
            
        except Exception as e:
            print(f"Error deleting link message: {e}")
