import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus


tag_proccess = []


emojis = [
    "🐶", "🐱", "🐭", "🐹", "🐰", "🐻", "🐼", "🐨", "🐵", "🐙", "🐸", "🐽", "🐷", "🐮", 
    "🦁", "🐯", "🙈", "🙉", "🙊", "🐒", "🐔", "🐧", "🐦", "🐤", "🦇", "🦄", "🐴", "🐗", 
    "🦊", "🐺", "🐥", "🐣", "🐝", "🦋", "🐛", "🐌", "🐞", "🐜", "🕷", "🦗", "🐟", "🐠", 
    "🐢", "🐍", "🦎", "🦀", "🦂", "🦟", "🐡", "🦈", "🐬", "🐳", "🐋", "🐊", "🐆", "🐅", 
    "🐄", "🐂", "🐃", "🦧", "🦍", "🦓", "🦒", "🐪", "🐫", "🐘", "🦏", "🦛", "🦘", "🦌", 
    "🦙", "🐓", "🐁", "🐀", "🐖", "🐎", "🐑", "🐏", "🐐", "🦃", "🕊", "🦅", "🦆", "🦉", 
    "🦩", "🦚", "🦨", "🐿", "🐇", "🐈", "🐩", "🦮", "🐕", "🦜", "🦝", "🦡", "🦔", "🦥", 
    "🦦", "🐾", "🐉", "🐲", "🧌", "🦖", "🦕", "🐚", "🍄", "🪿", "🐦‍⬛", "🐦‍🔥", "🫎", "🫏",
    "🔥", "✨", "💫", "⭐", "🌟", "💖", "💎", "⚡", "🍀", "🎉"
]

@Client.on_message(filters.command("all") & filters.group)
async def mention_all(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    status_msg = await message.reply_text("⏳ Admin ဟုတ်မဟုတ် စစ်ဆေးနေပါတယ်...")

    try:
        check_admin = await client.get_chat_member(chat_id, user_id)
        if check_admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await status_msg.edit_text("❌ ဒီ Command ကို Group Admin များသာ အသုံးပြုနိုင်ပါတယ်။")

        input_text = message.text.split(None, 1)
        custom_message = input_text[1] if len(input_text) > 1 else "မင်္ဂလာပါ အားလုံးပဲ လာကြပါဦး ✨"

        await status_msg.edit_text("🚀 Member များကို Tag ခေါ်ပေးနေပါပြီ...\n\n(ရပ်တန့်လိုပါက `/stop` ဟု ရိုက်ပါ)")

        
        tag_proccess.append(chat_id)

        members = []
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                
                rand_emoji = random.choice(emojis)
                emoji_mention = f"[{rand_emoji}](tg://user?id={member.user.id})"
                members.append(emoji_mention)

        count = 0
        total_members = len(members)
        
        
        for i in range(0, total_members, 10):
        
            if chat_id not in tag_proccess:
                break
                
            chunk = members[i:i+10]
            mention_string = " ".join(chunk) 
            
            try:
                await client.send_message(
                    chat_id,
                    f"**{custom_message}**\n\n"
                    f"{mention_string}"
                )
                count += len(chunk)
                await asyncio.sleep(2.5) 
            except Exception:
                break

        
        if chat_id in tag_proccess:
            tag_proccess.remove(chat_id)
            await status_msg.edit_text(f"✅ **Member {count} ယောက်ကို Tag ခေါ်ပြီးပါပြီ!**")
        else:
            await status_msg.edit_text(f"🛑 **Tag ခေါ်ခြင်းကို ရပ်တန့်လိုက်ပါပြီ။**\n(ခေါ်ပြီးသမျှ: `{count}` ယောက်)")
        
        await asyncio.sleep(10)
        await status_msg.delete()

    except Exception as e:
        if chat_id in tag_proccess: tag_proccess.remove(chat_id)
        await status_msg.edit_text(f"❌ Error: {e}")


@Client.on_message(filters.command("stop") & filters.group)
async def stop_tagging(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    
    check_admin = await client.get_chat_member(chat_id, user_id)
    if check_admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ Admin များသာ Tag ခေါ်ခြင်းကို ရပ်တန့်နိုင်ပါတယ်။")

    if chat_id in tag_proccess:
        tag_proccess.remove(chat_id)
        await message.reply_text("🛑 **Tag ခေါ်နေခြင်းကို ရပ်တန့်ရန် အမိန့်ပေးလိုက်ပါပြီ။**")
    else:
        await message.reply_text("💡 လက်ရှိမှာ Tag ခေါ်နေတာမျိုး မရှိပါဘူးဗျာ။")
