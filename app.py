import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ዋናው መነሻ ሜኑ (Start Menu)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🎮 ቢንጎ ጀምር", callback_data="start_bingo"),
        InlineKeyboardButton("💰 አካውንት (Balance)", callback_data="balance"),
        InlineKeyboardButton("📥 ዲፖዚት (Deposit)", callback_data="deposit"),
        InlineKeyboardButton("📤 ዊዝድሮ (Withdraw)", callback_data="withdraw")
    )
    bot.send_message(message.chat.id, "ሰላም! ወደ ቢንጎ እና ጨዋታ ቦት እንኳን ደህና መጡ። ከታች ያሉትን አማራጮች ይምረጡ:", reply_markup=markup)

# አዝራሮቹ ሲጫኑ የሚሰጡት ምላሾች
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "start_bingo":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🎮 የቢንጎ ጨዋታ ክፍለ ጊዜ እየተዘጋጀ ነው... እባክዎ ይጠብቁ!")
    elif call.data == "balance":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💰 የእርስዎ አካውንት ቀሪ ሂሳብ: 0.00 ብር")
    elif call.data == "deposit":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📥 ዲፖዚት ለማድረግ እባክዎ የባንክ አካውንት ቁጥር ይጠይቁ ወይም በቴሌብር ይክፈሉ።")
    elif call.data == "withdraw":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📤 ገንዘብ ለማውጣት (Withdraw) የሚፈልጉትን መጠን ይጻፉ:")

if __name__ == '__main__':
    bot.infinity_polling()
