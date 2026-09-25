import os
import telebot

# Railway পরিবেশ থেকে টোকেন সংগ্রহ করার কমান্ড
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# /start বা /help লিখলে বট যা উত্তর দেবে
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি আপনার নতুন বট। আমি সফলভাবে ক্লাউডে রান করছি!")

# ইউজার কোনো মেসেজ দিলে বট সেটিই রিপ্লাই দেবে
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "আপনার মেসেজ পেয়েছি: " + message.text)

# বট চালু রাখার কমান্ড
bot.polling()
