# bot.py 
import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from courses_config import COURSES, WELCOME_MESSAGE, NOT_FOUND_MESSAGE

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Build app
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    logger.info(f"📩 /start from user {user.id}, args: {args}")
    
    if not args:
        await update.message.reply_text(
            WELCOME_MESSAGE.format(first_name=user.first_name),
            parse_mode='Markdown'
        )
        return
    
    course_id = args[0]
    if course_id in COURSES:
        course = COURSES[course_id]
        await update.message.reply_text(f"📦 Sending: {course['title']}...")
        
        # Send first 5 links as example (expand as needed)
        for part in course['parts'][:5]:
            await update.message.reply_text(
                f"📥 [Part {part['num']}: {part['name']} ({part['size']})]({part['url']})",
                parse_mode='Markdown'
            )
        
        if len(course['parts']) > 5:
            await update.message.reply_text(
                f"⚠️ Showing 5 of {len(course['parts'])} parts. Visit website for all links."
            )
    else:
        await update.message.reply_text(NOT_FOUND_MESSAGE, parse_mode='Markdown')

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "*📚 Available Courses:*\n\n"
    for cid, info in COURSES.items():
        link = f"https://t.me/{context.bot.username}?start={cid}"
        text += f"• *{info['title']}*\n  [Get Links]({link})\n\n"
    await update.message.reply_text(text, parse_mode='Markdown')

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("courses", courses))

# Flask webhook server
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_flask(request.get_json())
    await app.process_update(update)
    return 'OK'

@flask_app.route('/')
def health():
    return '🤖 CFSD Bot is running!'

async def setup_webhook():
    """Set webhook before Flask starts"""
    if WEBHOOK_URL:
        await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        logger.info(f"✅ Webhook set: {WEBHOOK_URL}/webhook")

if __name__ == '__main__':
    logger.info("🚀 Starting CFSD Bot (Webhook Mode)...")
    
    # Run setup + Flask in async context
    async def run():
        await setup_webhook()
        # Run Flask in executor to not block asyncio
        import threading
        def run_flask():
            flask_app.run(host='0.0.0.0', port=PORT)
        thread = threading.Thread(target=run_flask, daemon=True)
        thread.start()
        # Keep alive
        while True:
            await asyncio.sleep(3600)
    
    asyncio.run(run())