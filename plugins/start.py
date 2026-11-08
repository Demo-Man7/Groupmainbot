import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


DEFAULT_PHOTO = "https://files.catbox.moe/ajn24w.jpg" 
WELCOME_STICKER = "CAACAgUAAxkBAAIe72mqfmL7cPOdiA5TOr6Gsih09cVTAALgGQACfA2YVRl1rlBfNwT5HgQ"

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    
    text = "𝒲ℯ𝓁𝒸ℴ𝓂ℯ ℬ𝒶𝒷𝓎"
    typing_msg = await message.reply_text("...")
    
    display_text = ""
    for char in text:
        display_text += char
        try:
            await typing_msg.edit_text(display_text)
            await asyncio.sleep(0.1) 
        except:
            pass
    
    await asyncio.sleep(1) 
    await typing_msg.delete()
    
    try:
        sent_stk = await message.reply_sticker(WELCOME_STICKER)
        await asyncio.sleep(5) 
        await sent_stk.delete() 
    except Exception as e:
        print(f"Sticker Error: {e}")

    
    user = message.from_user
    
    welcome_final = (
        f"**Welcome** {user.mention} ✨\n\n"
        "**Group Help Bot** မှ ကြိုဆိုပါတယ်ဗျာ။\n"
        "**Auto Reply နဲ့ Group Management Bot တစ်ခုဖြစ်ပါတယ်။**\n"
        "**အချစ်ရေးများလည်းမေးလို့ရပါတယ်** /happy /love /mylove **or** /couple **ဖြင့်**။\n"
        "**သိလိုရာများကို** /help **တွေကိုနှိပ်ပြီး လေ့လာနိုင်ပါတယ်ဗျာ။**"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝘾𝙝𝙖𝙣𝙣𝙚𝙡 📢", url="https://t.me/RoyalRebelsParty"),
            InlineKeyboardButton("𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧 👨‍💻", url="tg://resolve?domain=myaethaephyu&text=𝙃𝙚𝙮𝙃𝙚𝙡𝙡𝙤")
        ],
        [
            InlineKeyboardButton("𝙎𝙪𝙥𝙥𝙤𝙧𝙩 👥", url="https://t.me/ZaxbysFamily"),
            InlineKeyboardButton("🪩 𝙐𝙥𝙙𝙖𝙩𝙚", url="t.me/RoyalRebelsParty/650")
        ],
        [
            InlineKeyboardButton("𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url=f"https://t.me/{client.me.username}?startgroup=true")
        ]
    ])

    
    try:
        await message.reply_photo(
            photo=DEFAULT_PHOTO,
            caption=welcome_final,
            reply_markup=buttons
        )
    except Exception as e:
        await message.reply_text(welcome_final, reply_markup=buttons)
