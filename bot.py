<<<<<<< Updated upstream
# bot.py - DEBUG VERSION
=======
# bot.py - FIXED: Sync Flask webhook (no async views)
>>>>>>> Stashed changes
import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

# Logging - MORE VERBOSE
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed to DEBUG
)
logger = logging.getLogger(__name__)

<<<<<<< Updated upstream
logger.debug(f"TOKEN loaded: {'Yes' if TOKEN else 'No'}")
logger.debug(f"WEBHOOK_URL: {WEBHOOK_URL}")
logger.debug(f"PORT: {PORT}")

# Build bot application
try:
    app = Application.builder().token(TOKEN).build()
    logger.info("✅ Application built successfully")
except Exception as e:
    logger.error(f"❌ Failed to build application: {e}")
    raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Debug start handler"""
    logger.info(f"📩 /start received from user {update.effective_user.id}")
    
=======
# Build bot application
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
>>>>>>> Stashed changes
    user = update.effective_user
    args = context.args
    
    logger.debug(f"User: {user.first_name}, Args: {args}")
    
<<<<<<< Updated upstream
    try:
        if not args:
            await update.message.reply_text("👋 Bot is working! Send /start python101 to test.")
            logger.info("✅ Welcome message sent")
        else:
            await update.message.reply_text(f"📦 You requested: {args[0]}")
            logger.info(f"✅ Course request sent: {args[0]}")
    except Exception as e:
        logger.error(f"❌ Failed to send message: {e}")
        await update.message.reply_text("❌ Error occurred. Check logs.")

async def post_init(application: Application):
    """Set webhook on startup"""
    if WEBHOOK_URL:
        try:
            await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
            logger.info(f"✅ Webhook set to: {WEBHOOK_URL}/webhook")
        except Exception as e:
            logger.error(f"❌ Failed to set webhook: {e}")

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("courses", lambda u, c: u.message.reply_text("Courses command works!")))

if __name__ == '__main__':
    logger.info("🚀 Starting bot...")
    
    if WEBHOOK_URL:
        # Webhook mode (needs Flask)
        logger.warning("⚠️ Webhook mode requires Flask. Switching to polling for debug.")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        # Polling mode (simpler)
        app.run_polling(allowed_updates=Update.ALL_TYPES)
=======
    if not args:
        await update.message.reply_text(
            WELCOME_MESSAGE.format(first_name=user.first_name),
            parse_mode='Markdown'
        )
        return
    
    course_id = args[0]
    if course_id in COURSES:
        course = COURSES[course_id]
        await update.message.reply_text(
            f"📦 *{course['title']}*\n\n"
            f"💾 {course['total_size']} ({course['parts_count']} parts)\n"
            f"⏳ Preparing links...",
            parse_mode='Markdown'
        )
        
        # Send first 5 parts with links
        for part in course['parts'][:5]:
            await update.message.reply_text(
                f"📥 [Part {part['num']}: {part['name']} ({part['size']})]({part['url']})",
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        
        if len(course['parts']) > 5:
            await update.message.reply_text(
                f"⚠️ Showing 5 of {len(course['parts'])} parts.\n"
                f"Visit website for all links: https://cfsd-stack.github.io/",
                parse_mode='Markdown'
            )
    else:
        await update.message.reply_text(
            NOT_FOUND_MESSAGE, 
            parse_mode='Markdown'
        )

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List available courses"""
    text = "*📚 Available Courses:*\n\n"
    for cid, info in COURSES.items():
        link = f"https://t.me/{context.bot.username}?start={cid}"
        text += f"• *{info['title']}*\n"
        text += f"  💾 {info['total_size']} | {info['parts_count']} parts\n"
        text += f"  [📥 Get Links]({link})\n\n"
    
    await update.message.reply_text(
        text, 
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("courses", courses))

# Flask app (SYNC - no async views!)
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Sync webhook handler - processes update with asyncio.run()"""
    try:
        update = Update.de_flask(request.get_json())
        # Run the async processing in a new event loop
        asyncio.run(app.process_update(update))
        return 'OK', 200
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return 'Error', 500

@flask_app.route('/')
def health():
    """Health check endpoint"""
    return '🤖 CFSD Bot is running!', 200

@flask_app.route('/ready')
def ready():
    """Readiness probe for Render"""
    return 'Ready', 200

def setup_webhook_sync():
    """Set webhook using synchronous request"""
    if WEBHOOK_URL:
        import urllib.request
        import json
        webhook_url = f"{WEBHOOK_URL}/webhook"
        api_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
        try:
            with urllib.request.urlopen(api_url) as response:
                result = json.loads(response.read())
                if result.get('ok'):
                    logger.info(f"✅ Webhook set: {webhook_url}")
                else:
                    logger.error(f"❌ Webhook failed: {result}")
        except Exception as e:
            logger.error(f"❌ Failed to set webhook: {e}")

if __name__ == '__main__':
    logger.info("🚀 Starting CFSD Bot (Webhook Mode - Fixed)...")
    
    # Set webhook before starting Flask
    setup_webhook_sync()
    
    # Start Flask server (sync, no async complications)
    logger.info(f"🌐 Flask listening on port {PORT}")
    flask_app.run(host='0.0.0.0', port=PORT)
>>>>>>> Stashed changes
