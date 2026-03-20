import asyncio
from telegram import Bot

# Replace with your token
TOKEN = "YOUR_BOT_TOKEN"

async def upload_and_get_id(file_path):
    bot = Bot(token=TOKEN)
    # Send to yourself (use your numeric user ID)
    # You can get your ID by messaging @userinfobot
    MY_CHAT_ID = 123456789 
    
    with open(file_path, 'rb') as f:
        message = await bot.send_document(chat_id=MY_CHAT_ID, document=f)
        return message.document.file_id

async def main():
    files = {
        "python101": "local_files/python101.zip",
        "webdev": "local_files/webdev.zip"
    }
    
    print("🚀 Uploading files to Telegram to get IDs...\n")
    
    for course, path in files.items():
        try:
            file_id = await upload_and_get_id(path)
            print(f"✅ {course}: {file_id}")
        except Exception as e:
            print(f"❌ {course} failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())