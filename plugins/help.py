import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# Variable ထဲက OWNER_ID ကို နံပါတ်စာရင်း (List) အဖြစ် ယူမည်
OWNER_ID_STR = os.environ.get("OWNER_ID", "0")
OWNER_IDS = [int(i.strip()) for i in OWNER_ID_STR.split(",") if i.strip().isdigit()]

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # --- ၁။ User များအတွက် (လူတိုင်းသုံးလို့ရတာ) ---
    help_text = "✨ **Bot Help Menu** ✨\n"
    help_text += "━━━━━━━━━━━━━━━━━━\n\n"
    help_text += "👤 **User Commands:**\n"
    help_text += "• `/id` - မိမိ ID ကိုကြည့်ရန်\n"
    help_text += "• `/couple` - groupတွင်သုံးရန်\n"
    help_text += "• `/happy` - groupတွင်ကြည့်ရန်\n"
    help_text += "• `/mylove` - အချစ်ရေးဟောရန်\n"
    help_text += "• `/love` - အချစ်ရေးဟောရန်\n\n"

    # --- ၂။ Admin များအတွက် စစ်ဆေးခြင်း ---
    is_admin = False
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        try:
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                is_admin = True
        except Exception:
            pass

    # Owner ဖြစ်မဖြစ် စစ်ရန် (List ထဲမှာ ပါမပါ စစ်သည်)
    is_owner = user_id in OWNER_IDS

    if is_admin or is_owner:
        help_text += "👮 **Admin Commands:**\n"
        help_text += "• `/all` - အဖွဲ့ဝင်အားလုံးကို Tag ခေါ်ရန်\n\n"

    # --- ၃။ Owner အတွက်သာ စစ်ဆေးခြင်း ---
    if is_owner:
        help_text += "👑 **Owner Commands:**\n"
        help_text += "• `/broadcast` - သတင်းစကားပါးရန်\n\n"

    help_text += "━━━━━━━━━━━━━━━━━━\n"
    help_text += "💡 _Command များကို အသုံးပြုရန် စာရိုက်ကွက်တွင် ရိုက်ထည့်ပါ_"

    await message.reply_text(help_text)
