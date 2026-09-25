import os
import telebot
import subprocess
import urllib.request
import shutil  # জিপ (zip) তৈরি এবং ফোল্ডার ডিলিট করার জন্য নতুন লাইব্রেরি

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

APKTOOL_JAR = "apktool.jar"
APKTOOL_URL = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar"

if not os.path.exists(APKTOOL_JAR):
    print("Apktool ডাউনলোড হচ্ছে...")
    try:
        urllib.request.urlretrieve(APKTOOL_URL, APKTOOL_JAR)
        print("Apktool ডাউনলোড সফল!")
    except Exception as e:
        print("Apktool ডাউনলোড ফেইল করেছে:", e)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমাকে যেকোনো ছোট সাইজের APK ফাইল দিন, আমি সেটি আনপ্যাক করে জিপ (ZIP) ফাইলে আপনাকে পাঠিয়ে দেব।")

@bot.message_handler(content_types=['document'])
def handle_apk(message):
    try:
        file_name = message.document.file_name
        if not file_name.endswith('.apk'):
            bot.reply_to(message, "অনুগ্রহ করে শুধুমাত্র .apk ফাইল দিন।")
            return
        
        bot.reply_to(message, "APK পেয়েছি, ডাউনলোড হচ্ছে...")
        
        # টেলিগ্রাম থেকে ফাইল ডাউনলোড
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.send_message(message.chat.id, "ডাউনলোড শেষ। আনপ্যাক করা হচ্ছে...")
        
        output_folder = file_name.replace('.apk', '_unpacked')
        result = subprocess.run(["java", "-jar", APKTOOL_JAR, "d", file_name, "-o", output_folder, "-f"], capture_output=True, text=True)
        
        if result.returncode == 0:
            bot.send_message(message.chat.id, "আনপ্যাক সফল হয়েছে! এখন জিপ (ZIP) করা হচ্ছে...")
            
            # আনপ্যাক করা ফোল্ডারটিকে জিপ ফাইলে রূপান্তর করা
            zip_filename = output_folder + ".zip"
            shutil.make_archive(output_folder, 'zip', output_folder)
            
            # জিপ ফাইলটি টেলিগ্রামে সেন্ড করা
            with open(zip_filename, 'rb') as zip_file:
                bot.send_document(message.chat.id, zip_file)
            
            bot.send_message(message.chat.id, "ফাইল সফলভাবে পাঠানো হয়েছে! 🎉")
            
            # কাজ শেষে সার্ভার থেকে ফাইলগুলো মুছে ফেলা (যাতে স্টোরেজ ফুল না হয়)
            os.remove(file_name)
            os.remove(zip_filename)
            shutil.rmtree(output_folder)
            
        else:
            bot.send_message(message.chat.id, f"আনপ্যাক করতে সমস্যা হয়েছে:\n{result.stderr[-200:]}")
            
    except Exception as e:
        bot.reply_to(message, f"কোনো সমস্যা হয়েছে: {str(e)}")

bot.polling()
