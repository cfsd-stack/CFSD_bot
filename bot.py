# bot.py
import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from courses_config import COURSES, WELCOME_MESSAGE, NOT_FOUND_MESSAGE

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-app.onrender.com
PORT = int(os.getenv("PORT", 8080))

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Build bot application
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with deep-linking for courses"""
    user = update.effective_user
    args = context.args
    
    # No course parameter - show welcome
    if not args:
        await update.message.reply_text(
            WELCOME_MESSAGE.format(first_name=user.first_name),
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        return
    
    # Course request via deep link
    course_id = args[0]
    logger.info(f"User {user.id} requested course: {course_id}")
    
    if course_id in COURSES:
        course = COURSES[course_id]
        
        # Send confirmation message
        await update.message.reply_text(
            f"📦 *{course['title']}*\n\n"
            f"📝 {course['description']}\n"
            f"💾 Total: {course['total_size']} ({course['parts_count']} parts)\n\n"
            f"⏳ Preparing download links...",
            parse_mode='Markdown'
        )
        
        # Send first 10 parts with inline buttons
        keyboard = []
        for part in course['parts'][:10]:
            keyboard.append([InlineKeyboardButton(
                f"📥 Part {part['num']}: {part['name']} ({part['size']})",
                url=part['url']
            )])
        
        # Add "show more" button if there are more parts
        if len(course['parts']) > 10:
            keyboard.append([InlineKeyboardButton(
                f"➕ Show {len(course['parts'])-10} More Parts",
                callback_data=f"more_{course_id}"
            )])
        
        # Add community invite button
        keyboard.append([InlineKeyboardButton(
            "💬 Join Community",
            url=course['channel_invite']
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "*📂 Download Links (1-10):*",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        # Send remaining parts as text (if any)
        if len(course['parts']) > 10:
            remaining_text = "*📂 Remaining Parts:*\n\n"
            for part in course['parts'][10:]:
                remaining_text += f"• [Part {part['num']}: {part['name']} ({part['size']})]({part['url']})\n"
            
            await update.message.reply_text(
                remaining_text,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        
        logger.info(f"Successfully sent course {course_id} to user {user.id}")
        
    else:
        await update.message.reply_text(
            NOT_FOUND_MESSAGE,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        logger.warning(f"User {user.id} requested invalid course: {course_id}")

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all available courses"""
    text = "*📚 Available Courses:*\n\n"
    
    for cid, info in COURSES.items():
        deep_link = f"https://t.me/{context.bot.username}?start={cid}"
        text += f"• *{info['title']}*\n"
        text += f"  {info['description']}\n"
        text += f"  💾 {info['total_size']} | {info['parts_count']} parts\n"
        text += f"  [📥 Get Links]({deep_link})\n\n"
    
    text += f"💬 Join our community: @cfsd_community"
    
    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

async def show_more_parts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback for showing remaining course parts"""
    query = update.callback_query
    await query.answer()
    
    course_id = query.data.split("_")[1]
    course = COURSES.get(course_id)
    
    if course:
        text = f"*📂 All Download Links - {course['title']}*\n\n"
        
        for i, part in enumerate(course['parts'], 1):
            text += f"{i}. [Part {part['num']}: {part['name']} ({part['size']})]({part['url']})\n"
        
        await query.message.edit_text(
            text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    else:
        await query.message.edit_text("❌ Course not found.")

async def post_init(application: Application):
    """Set webhook on startup (for Render deployment)"""
    if WEBHOOK_URL:
        await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        logger.info(f"✅ Webhook set to: {WEBHOOK_URL}/webhook")

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("courses", courses))
app.add_handler(CallbackQueryHandler(show_more_parts, pattern="^more_"))

# Flask app for webhook
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    """Receive updates from Telegram"""
    update = Update.de_flask(request.get_json())
    await app.process_update(update)
    return 'OK'

@flask_app.route('/')
def health():
    """Health check endpoint for Render"""
    return '🤖 CFSD Bot is running!'

@flask_app.route('/ready', methods=['GET'])
def ready():
    """Kubernetes/Render readiness probe"""
    return 'Ready', 200

if __name__ == '__main__':
    logger.info("🚀 Starting CFSD Courses Bot...")
    
    # Run Flask app (webhook mode for Render)
    flask_app.run(host='0.0.0.0', port=PORT)