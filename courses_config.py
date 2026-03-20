# courses_config.py
# Store all your GoFile links here - update without redeploying bot code!

COURSES = {
    "python101": {
        "title": "Python Mastery Course",
        "description": "Complete Python course from beginner to advanced",
        "total_size": "50 GB",
        "parts_count": 25,
        "channel_invite": "https://t.me/+WGXY_t9f9jYzN2Y6",  # Your community channel
        "parts": [
            {"num": 1, "url": "https://gofile.io/d/AbCdEf", "size": "2 GB", "name": "Intro & Setup"},
            {"num": 2, "url": "https://gofile.io/d/XyZ123", "size": "2 GB", "name": "Python Basics"},
            {"num": 3, "url": "https://gofile.io/d/QwErTy", "size": "2 GB", "name": "Data Types"},
            # ... add all 25 parts here
            {"num": 25, "url": "https://gofile.io/d/FiNaL1", "size": "2 GB", "name": "Final Project"},
        ]
    },
    "webdev": {
        "title": "Web Development Bootcamp",
        "description": "Full-stack web development course",
        "total_size": "45 GB",
        "parts_count": 23,
        "channel_invite": "https://t.me/+WGXY_t9f9jYzN2Y6",
        "parts": [
            {"num": 1, "url": "https://gofile.io/d/WebD01", "size": "2 GB", "name": "HTML Basics"},
            # ... add all parts
        ]
    },
    # Add more courses as needed
}

# Welcome message for users without course parameter
WELCOME_MESSAGE = """
👋 Hi {first_name}!

📚 Welcome to CFSD Courses Bot!

To download a course:
1️⃣ Visit our website: https://cfsd-stack.github.io/
2️⃣ Click "Get Links via Telegram" on any course
3️⃣ I'll send you all download links organized!

💬 Join our community: @cfsd_community

Type /courses to see available courses.
"""

# Message shown when course not found
NOT_FOUND_MESSAGE = """
❌ Course not found!

Please visit our website to get valid download links:
https://cfsd-stack.github.io/

Or type /courses to see available courses.
"""