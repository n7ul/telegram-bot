import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك! أرسل لي رابطًا من أي منصة وسأعطيك رابط التحميل 🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # تحقق إذا الرسالة رابط
    if not url.startswith("http"):
        await update.message.reply_text("❌ أرسل رابطًا صحيحًا من تيك توك أو يوتيوب أو إنستغرام...")
        return

    # رابط API خارجي لتحميل الفيديوهات
    api_url = f"https://save-from.net/api/convert?url={url}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'url' in data and data['url']:
            download_link = data['url']
            await update.message.reply_text(f"📝 نص مستخرج:\n{download_link}")
        else:
            await update.message.reply_text("❌ لم أستطع استخراج الرابط، جرب رابط آخر.")
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء المعالجة.")
        print(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
