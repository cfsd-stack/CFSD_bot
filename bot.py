# bot.py - DEBUG VERSION
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
    
    user = update.effective_user
    args = context.args
    
    logger.debug(f"User: {user.first_name}, Args: {args}")
    
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