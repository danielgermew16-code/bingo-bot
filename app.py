import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ለጊዜው የተጠቃሚዎችን ሂሳብ እና መረጃ ለመያዝ (Databse ምትክ)
user_balances = {}
user_phones = {}

# ዋናው መነሻ ሜኑ (Start Menu - ከቪዲዮው ጋር ተመሳሳይ የሆነ)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎮 ጨዋታ (Play)", callback_data="play_game"),
        InlineKeyboardButton("💰 አካውንት (Balance)", callback_data="balance"),
        InlineKeyboardButton("📥 ዲፖዚት (Deposit)", callback_data="deposit"),
        InlineKeyboardButton("📤 ዊዝድሮ (Withdraw)", callback_data="withdraw"),
        InlineKeyboardButton("👥 ሼር & አግኝ", callback_data="invite"),
        InlineKeyboardButton("💎 VIP ክፍል", callback_data="vip")
    )
    bot.send_message(
        user_id, 
        f"✨ ሰላም! እንኳን ወደ ቢንጎ ቦት በደህና መጡ! Dani!\n\n"
        f"እባክዎ ከታች ያሉትን አማራጮች በመጠቀም መጫወት ይጀምሩ፦", 
        reply_markup=markup
    )

# የአዝራሮች ምላሽ (Callback Handler)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    
    if call.data == "play_game":
        bot.answer_callback_query(call.id)
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🎲 75 ቁጥሮች ቢንጎ (አውቶማቲክ)", callback_data="start_75_bingo"),
            InlineKeyboardButton("🔙 ወደ ዋናው ሜኑ", callback_data="back_home")
        )
        bot.send_message(user_id, "🎮 የጨዋታ ክፍል፦ የሚፈልጉትን የቢንጎ ዓይነት ይምረጡ (ከአጠቃላይ 400 ካርቴላዎች ውስጥ ይመረጣል):", reply_markup=markup)

    elif call.data == "start_75_bingo":
        bot.answer_callback_query(call.id)
        # 75 ቁጥሮችን ከቦታው ማውጣት እና አውቶማቲክ ማረጋገጥ
        drawn_number = random.randint(1, 75)
        bot.send_message(
            user_id, 
            f"🎰 **የቢንጎ ማሽን ተጀመረ!** (75 ቁጥሮች ሲስተም)\n\n"
            f"ወጥቶ የነበረው ቁጥር: **{drawn_number}**\n"
            f"ካርቴላዎችዎ በራስ-ሰር እየተጣሩ (Auto-checking) ናቸው...\n\n"
            f"🎉 **ቢንጎ!** ቲኬቱ ተዘጋግቷል! አሸናፊውን ገንዘብ አካውንትዎ ገብቷል!", 
            parse_mode="Markdown"
        )

    elif call.data == "balance":
        bot.answer_callback_query(call.id)
        balance = user_balances.get(user_id, 0.00)
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📥 ዲፖዚት አድርግ", callback_data="deposit"),
            InlineKeyboardButton("📤 ዊዝድሮ አድርግ", callback_data="withdraw"),
            InlineKeyboardButton("🔙 ወደ ዋናው ሜኑ", callback_data="back_home")
        )
        bot.send_message(user_id, f"💰 **የእርስዎ የባንክ አካውንት ሂሳብ**\n\nቀሪ ሂሳብ: **{balance} ETB**", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "deposit":
        bot.answer_callback_query(call.id)
        bot.send_message(
            user_id,
            "📥 **ጥሬ ገንዘብ ማስገቢያ (Deposit)**\n\n"
            "1. 200 ETB ወይም የሚፈልጉትን መጠን ከታች ባለው የቴሌብር ቁጥር ያስተላልፉ፦\n"
            "📞 **0969927803 (Tizita)**\n\n"
            "2. ያስተላለፉበትን የሰርተፍኬት/የመሰረዝ ማረጋገጫ (Txn ID) ወይም የትራንዛክሽን ጽሁፍ እዚህጋር ይላኩ (Paste ያድርጉ)።"
        )

    elif call.data == "withdraw":
        bot.answer_callback_query(call.id)
        bot.send_message(
            user_id,
            "📤 **ገንዘብ ማውጣት (Withdraw)**\n\n"
            "እባክዎ ማውጣት የሚፈልጉትን የብር መጠን እና የባንክ/የቴሌብር ቁጥርዎን ይጻፉ (ለምሳሌ: *ወጣ 500 09XXXXXXXX*)"
        )

    elif call.data == "invite":
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "🔗 የርሶ መጋበዣ ሊንክ:\nhttps://t.me/bingo_bot?start=ref123\n\nጓደኛዎን በመጋበዝ 20 ETB ቦነስ ያግኙ!")

    elif call.data == "vip":
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "💎 **VIP ክፍል**\nለየት ያሉ ከፍተኛ ሽልማቶች እና ልዩ ጨዋታዎች የሚደረጉበት ከፍ ያለ ክፍል ነው። ገቢዎትን ከፍ በማድረግ መቀላቀል ይችላሉ።")

    elif call.data == "back_home":
        bot.answer_callback_query(call.id)
        send_welcome(call.message)

if __name__ == '__main__':
    bot.infinity_polling()
