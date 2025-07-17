import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# الطريقة الأكيدة لقراءة التوكن
BOT_TOKEN = os.getenv('BOT_TOKEN') or "7878923171:AAECMA13-eO_zS7b-GocbbKlCN3PXJi_5g0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 البوت يعمل الآن!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📩: {update.message.text}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, echo))
print("✅ تم التشغيل بنجاح")
app.run_polling()