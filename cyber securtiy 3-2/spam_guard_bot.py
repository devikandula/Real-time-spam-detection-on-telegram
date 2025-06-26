from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
import mysql.connector
import re

# 🔐 Replace with your new secure token from BotFather
BOT_TOKEN = '7479246329:AAGcnVHs8qbRge5GZN21jKwqC-SZLyYGsao'

SPAM_KEYWORDS = [
    'free', 'crypto', 'join now', 'click here', 'buy now', 'earn money',
    'p@rt-t!me', '0pportunity', 'investment', 'd@ily', 'n0 fees',
    'c@sh', 'b0nus', 'unlock', 'h!gh-paying', 'w0rk', 'instant money',
    'sk!lls', 'r3ply yes'
]
LINK_REGEX = r'https?://\S+'

MAX_MESSAGES = 3
TIME_WINDOW = timedelta(seconds=10)
user_message_log = {}

# ✅ MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pandu@2004",
    database="spam_guard"
)
cursor = db.cursor()

def log_to_db(username, user_id, message, action): # type: ignore
    try:
        sql = "INSERT INTO spam_logs (username, user_id, message, action, log_time) VALUES (%s, %s, %s, %s, %s)"
        val = (username, user_id, message, action, datetime.now())# type: ignore
        cursor.execute(sql, val)# type: ignore
        db.commit()
    except Exception as e:
        print(f"❌ DB Error: {e}")

async def detect_spam(update: Update, context: ContextTypes.DEFAULT_TYPE): # type: ignore
    if not update.message or not update.message.text:
        return

    user = update.message.from_user
    user_id = user.id
    username = user.username or f"id_{user_id}"
    chat_id = update.message.chat_id
    text = update.message.text.lower()

    now = datetime.now()
    user_message_log.setdefault(user_id, []).append(now) # type: ignore
    user_message_log[user_id] = [t for t in user_message_log[user_id] if now - t < TIME_WINDOW] # type: ignore

    try:
        member = await context.bot.get_chat_member(chat_id, user_id) # type: ignore
        is_admin = member.status in ['administrator', 'creator']
    except:
        is_admin = False

    is_spam = (
        any(kw in text for kw in SPAM_KEYWORDS)
        or re.search(LINK_REGEX, text)
        or len(user_message_log[user_id]) > MAX_MESSAGES # type: ignore
    )

    action_taken = ""
    if is_spam:
        try:
            await update.message.delete()
            action_taken = "Message deleted"

            if not is_admin:
                await context.bot.restrict_chat_member( # type: ignore
                    chat_id, user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=now + timedelta(minutes=1)
                )
                await context.bot.send_message( # type: ignore
                    chat_id,
                    f"🚨 Spam alert: @{username} muted for 1 minute."
                )
                action_taken += " + User muted"
            else:
                await context.bot.send_message( # type: ignore
                    chat_id,
                    f"⚠️ Warning: @{username} (admin)'s spam message was deleted."
                )
                action_taken += " (admin - not muted)"

        except Exception as e:
            action_taken = f"Error: {e}"

        log_to_db(username, user_id, text, action_taken)
        print(f"Action: {action_taken} | User: @{username}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build() # type: ignore
    print("🚀 SpamGuardHelperBot is running with MySQL logging...")

    spam_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, detect_spam) # type: ignore
    app.add_handler(spam_handler) # type: ignore

    app.run_polling()
