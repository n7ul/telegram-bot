#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, asyncio, tempfile, shutil, cv2, pytesseract
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")

class SocialMediaDownloader:
    def __init__(self):
        self.supported_sites = ['youtube.com','youtu.be','instagram.com','facebook.com',
                                'twitter.com','x.com','tiktok.com','snapchat.com',
                                'reddit.com','vimeo.com','dailymotion.com']
        self.max_size = 50*1024*1024
    def is_supported(self, url):
        return any(s in url.lower() for s in self.supported_sites)
    def download(self, url, path):
        opts = {'format':'best[height<=720][filesize<50M]/best[height<=480][filesize<50M]',
                'outtmpl':path+'/%(title)s.%(ext)s','restrictfilenames':True,
                'noplaylist':True,'no_warnings':True,'ignoreerrors':True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = (info.get('title') or 'video')[:50]
            ydl.download([url])
            for f in os.listdir(path):
                if f.endswith(('.mp4','.mkv','.webm','.avi','.mov')):
                    fp = os.path.join(path, f)
                    if os.path.getsize(fp) < self.max_size:
                        return fp, title
        raise Exception("File issue")

    def extract_text(self, video):
        cap = cv2.VideoCapture(video)
        if not cap.isOpened(): return "❌ Cannot open video"
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        texts = []
        for rs in [0.1,0.5,0.9]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(total*rs))
            ret, frm = cap.read()
            if not ret: continue
            gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            text_ar = pytesseract.image_to_string(gray, lang='ara', config='--psm 6').strip()
            text_en = pytesseract.image_to_string(gray, lang='eng', config='--psm 6').strip()
            if text_ar and len(text_ar)>3: texts.append("🔤 عربي: "+text_ar)
            if text_en and len(text_en)>3: texts.append("🔤 English: "+text_en)
        cap.release()
       return "📝 نص مستخرج:" 
"+ "

".join(dict.fromkeys(texts)) if texts else "ℹ️ لا يوجد نص واضح"

async def cmd_start(up: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await up.message.reply_text("🤖 أهلاً! أرسل رابط فيديو وسأقوم بالتنزيل والاستخراج.")

async def on_message(up: Update, ctx: ContextTypes.DEFAULT_TYPE):
    url = up.message.text.strip()
    if not downloader.is_supported(url):
        return await up.message.reply_text("❌ غير مدعوم.")
    tdir = tempfile.mkdtemp()
    try:
        await up.message.reply_text("📥 جاري التنزيل...")
        video, title = downloader.download(url, tdir)
        text = downloader.extract_text(video)
        await up.message.reply_video(open(video,'rb'), caption=title)
        await up.message.reply_text(text)
    except Exception as e:
        await up.message.reply_text("❌ خطأ: "+str(e))
    finally:
        shutil.rmtree(tdir)

downloader = SocialMediaDownloader()

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    app.run_polling()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"
    main()
