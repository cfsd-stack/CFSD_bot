import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from courses_config import COURSES

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Env Vars
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-app.onrender.com
PORT = int(os.getenv("PORT", 8080))

# Bot App
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user = update.effective_user

    if not args:
        await update.message.reply_text(
            f"👋 Hi {user.first_name}!\nClick a download link on our website to get files here."
        )
        return

    course_id = args[0]
    
    if course_id in COURSES:
        course = COURSES[course_id]
        await update.message.reply_text(f"📚 Sending: {course['title']}...")
        
        try:
            # Send using file_id (Instant, no upload)
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=course['file_id'],
                caption=course['caption']
            )
        except Exception as e:
            logger.error(e)
            await update.message.reply_text("❌ Error sending file. Contact support.")
    else:
        await update.message.reply_text("❌ Course not found.")

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📚 Available Courses:\n\n"
    for cid, info in COURSES.items():
        link = f"https://t.me/{context.bot.username}?start={cid}"
        text += f"• {info['title']}\n  [Download]({link})\n\n"
    await update.message.reply_text(text, parse_mode='Markdown')

# Register Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("courses", courses))

# Flask Webhook Server
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_flask(request.get_json())
    await app.process_update(update)
    return 'OK'

@flask_app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    # Set webhook on startup
    asyncio.run(app.bot.set_webhook(f"{WEBHOOK_URL}/webhook"))
    logger.info(f"🚀 Starting webhook on port {PORT}")
    flask_app.run(host='0.0.0.0', port=PORT)