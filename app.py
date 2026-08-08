import os
import telebot

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! የቢንጎ ቦትዎ በትክክል እየሰራ ነው። 🎮")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "መልዕክትዎ ደርሶኛል!")

if __name__ == '__main__':
    bot.infinity_polling()
