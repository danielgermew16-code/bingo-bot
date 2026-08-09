import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# የሰጡትን የቦት ቶክን እዚህ አስገብቻለሁ
TOKEN = '8675696315:AAElsrJ58XnL-lbUEl5EHhUbdfdRyUp5i04'
bot = telebot.TeleBot(TOKEN)

# የቴሌብር ቁጥር እና የክፍያ መረጃ
TELEBIRR_NUMBER = "0969927803"

# የመነሻ ሜኑ
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🎮 ቢንጎ መጫወት ጀምር", callback_data="play_bingo"),
        InlineKeyboardButton("💰 ሂሳብ ማስገባት (Deposit)", callback_data="deposit")
    )
    markup.add(
        InlineKeyboardButton("💳 የባንክ/ቴሌብር ሒሳብ", callback_data="balance"),
        InlineKeyboardButton("📤 ገንዘብ ማውጣት (Withdraw)", callback_data="withdraw")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        f"ሰላም <b>{message.from_user.first_name}</b>! ወደ ቢንጎ ቦት እንኳን ደህና መጡ።\n\n"
        "ከታች ባሉት አማራጮች በመጠቀም መጫወት እና ሂሳብዎን መቆጣጠር ይችላሉ።"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "play_bingo":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "🎲 <b>የቢንጎ ጨዋታ</b>\n\nእባክዎ የሚፈልጉትን የካርቴላ ዋጋ ይምረጡ:",
            parse_mode='HTML',
            reply_markup=bingo_rooms_menu()
        )
    elif call.data == "deposit":
        bot.answer_callback_query(call.id)
        deposit_text = (
            "💰 <b>ሂሳብ ለማስገባት (Deposit):</b>\n\n"
            f"እባክዎ የሚፈልጉትን ገንዘብ ከዚህ በታች ባለው የቴሌብር ቁጥር ያስተላልፉ:\n\n"
            f"📱 <b>ቴሌብር ቁጥር:</b> <code>{TELEBIRR_NUMBER}</code>\n"
            "👤 <b>ስም:</b> በሰናይ ስም\n\n"
            "ክፍያውን ከፈጸሙ በኋላ የትራንዛክሽን ደረሰኝ (Screenshot) ለአስተዳዳሪው በመላክ አካውንትዎ ላይ ቀሪ ሂሳብ እንዲሞላ ያድርጉ።"
        )
        bot.send_message(call.message.chat.id, deposit_text, parse_mode='HTML', reply_markup=back_to_menu())
    elif call.data == "balance":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "💳 <b>የእርስዎ ቀሪ ሂሳብ:</b> 0.00 ETB\n\nሂሳብዎ ባዶ ነው። እባክዎ በመጀመሪያ ገንዘብ ያስገቡ።",
            parse_mode='HTML',
            reply_markup=back_to_menu()
        )
    elif call.data == "withdraw":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📤 <b>ገንዘብ ለማውጣት:</b>\n\nለማውጣት የሚችሉት ዝቅተኛው የብር መጠን 50 ETB ነው። ቀሪ ሂሳብዎ በቂ አይደለም።",
            parse_mode='HTML',
            reply_markup=back_to_menu()
        )
    elif call.data == "main_menu":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="እንኳን ደህና መጡ! የሚፈልጉትን አማራጭ ይምረጡ፡",
            reply_markup=main_menu()
        )

def bingo_rooms_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🥉 ክፍል 1 (10 ብር)", callback_data="room_10"),
        InlineKeyboardButton("🥈 ክፍል 2 (25 ብር)", callback_data="room_25"),
        InlineKeyboardButton("🥇 ክፍል 3 (50 ብር)", callback_data="room_50"),
        InlineKeyboardButton("🔙 ወደ ዋናው ሜኑ", callback_data="main_menu")
    )
    return markup

def back_to_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 ወደ ዋናው ሜኑ", callback_data="main_menu"))
    return markup

# ቦቱን ማስጀመር
print("ቦቱ በተሳካ ሁኔታ ተጀምሯል እና በመሥራት ላይ ነው...")
bot.infinity_polling()
