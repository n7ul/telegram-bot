import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "tiktok.com" in text:
        url = f"https://api.tiklydown.me/api/download?url={text}"
        res = requests.get(url).json()
        download_link = res.get("video", {}).get("url", "")
    elif "instagram.com" in text:
        url = f"https://saveig.app/api/ajaxSearch"
        res = requests.post(url, data={"q": text}).json()
        download_link = res["data"][0]["url"] if "data" in res else ""
    elif "youtube.com" in text or "youtu.be" in text:
        url = f"https://you-link.vercel.app/api/?url={text}"
        res = requests.get(url).json()
        download_link = res["link"][0]["url"] if "link" in res else ""
    elif "twitter.com" in text or "x.com" in text:
        url = f"https://tweetpik.com/api/tweet/video?url={text}"
        res = requests.get(url).json()
        download_link = res["variants"][0]["url"] if "variants" in res else ""
    elif "facebook.com" in text:
        url = f"https://saveas.co/api/fb?url={text}"
        res = requests.get(url).json()
        download_link = res.get("url", "")
    else:
        download_link = ""

    if download_link:
        await update.message.reply_text(f"📝 نص مستخرج:\n{download_link}")
    else:
        await update.message.reply_text("لم أستطع استخراج الرابط من هذا الرابط، جرب رابطًا آخر.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
