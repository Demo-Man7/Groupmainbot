import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("mylove") & filters.group)
async def find_my_love(client: Client, message: Message):
    chat_id = message.chat.id
    user_mention = message.from_user.mention
    
    
    members = []
    async for member in client.get_chat_members(chat_id, limit=100):
        
        if not member.user.is_bot and member.user.id != message.from_user.id:
            members.append(member.user)

    
    if len(members) < 1:
        return await message.reply_text("⚠️  ဒီ Group ထဲမှာ သင်တစ်ယောက်တည်းပဲ ရှိနေလို့ ရှာမတွေ့နိုင်သေးပါဘူးဗျာ။")

    
    soulmate = random.choice(members)
    soulmate_mention = soulmate.mention

    
    love_texts = [
        f"💕 {user_mention} ရေ... \nသင့်ရဲ့ ရှာဖွေနေသော ဖူးစာဖက်လေးကတော့ {soulmate_mention} ပဲ ဖြစ်ပါတယ်ခင်ဗျာ။",
        f"💓 ဝိုး... {user_mention} နဲ့ {soulmate_mention} ကတော့ \nတကယ့်ကို လိုက်ဖက်ညီတဲ့ စုံတွဲလေးပါပဲဗျာ။",
        f"💞 {user_mention} ရဲ့ နှလုံးသားပိုင်ရှင်လေးကို ရှာတွေ့ပါပြီ!\n သူကတော့ {soulmate_mention} ပါတဲ့ဗျ။",
        f"💘 ***ဖူးစာရှင်နတ်သားလေး***က ဖန်တီးပေးလိုက်တဲ့\n {user_mention} ရဲ့ တစ်သက်တာ အဖော်မွန်ကတော့ {soulmate_mention} ပါပဲ။"
    ]
    
    
    msg = await message.reply_text("💘ဖူးစာရှင်ကို ရှာဖွေနေပါသည်... ခေတ္တစောင့်ပါ။💕\n💞 ထားခဲ့သူကို မေ့ဖို့ ကူညီပေးပါမယ် 🎁")
    await asyncio.sleep(2)
    
    
    await msg.edit(random.choice(love_texts))
