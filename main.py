import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# نحصل على التوكن من متغير البيئة في Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك! أرسل لي رابطًا أو رسالة.")

# أمر /get
async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هنا نرد بالجملة المطلوبة
    return_text = "📝 نص مستخرج:"
    await update.message.reply_text(return_text)

# نبدأ البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_text))

    app.run_polling()

if __name__ == "__main__":
    main()
