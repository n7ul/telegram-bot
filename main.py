import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("http"):
        await update.message.reply_text(f"📝 تم استلام الرابط:\n{text}")
    else:
        await update.message.reply_text("أرسل لي رابطًا من تيك توك، إنستغرام، أو يوتيوب.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
