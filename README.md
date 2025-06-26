# 🤖 SpamGuardHelperBot - Real-Time Spam Detection on Telegram

This project is a real-time spam detection bot for **Telegram** groups, designed using Python and integrated with a **MySQL** database for logging. It helps group administrators automatically moderate chats by detecting spam messages based on keywords, links, and message flooding patterns.

## 📌 Project Overview

Telegram is increasingly exploited by spammers to spread phishing links, fake job offers, crypto scams, and unsolicited promotions. **SpamGuardHelperBot** aims to counter this by:

- Automatically deleting suspicious messages.
- Muting offending users (except admins) for a brief period.
- Logging all actions to a MySQL database for transparency and future analysis.

> 🔒 All spam detection and moderation are handled in real-time to ensure the safety and usability of group discussions.

## 🎯 Features

- ✅ **Keyword-Based Filtering**
- 🌐 **Suspicious Link Detection**
- 📈 **Flood Detection** (based on message frequency)
- 🛡️ **Admin Role Check** (prevents muting admins)
- 🗃️ **MySQL Logging** for all spam incidents
- 🧩 **Easily Customizable Spam Rules**

## 📁 Project Structure

```
spam_guard/
│
├── spam_guard_bot.py        # Main bot logic and spam detection
├── spam_guard.txt           # SQL script for MySQL table creation and keywords
├── Mini Project 3 First Review.pptx   # Initial project presentation
├── Mini Project 3 Final Review.pptx   # Final project presentation
```

## ⚙️ Technologies Used

- **Python**
- **python-telegram-bot v20+**
- **MySQL**
- **Regex**
- **Datetime**

## 🧠 How It Works

1. User messages are analyzed for:
   - Predefined spam keywords (e.g., "free", "click here", "crypto")
   - Links (`http://`, `https://`)
   - High-frequency message bursts (flooding)
2. If spam is detected:
   - The message is deleted.
   - The user is muted for 1 minute (if not an admin).
   - Actions are logged into the `spam_logs` table.

## 🗃️ MySQL Schema

```sql
CREATE TABLE spam_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    user_id BIGINT,
    message TEXT,
    action VARCHAR(255),
    log_time DATETIME
);

CREATE TABLE spam_keywords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL UNIQUE
);

-- Sample spam keywords
INSERT INTO spam_keywords (keyword)
VALUES ('free'), ('crypto'), ('join now'), ('click here'), ('buy now'), ('earn money');
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL Server
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone this repository**

```bash
git clone https://github.com/yourusername/spamguard-bot.git
cd spamguard-bot
```

2. **Install dependencies**

```bash
pip install python-telegram-bot mysql-connector-python
```

3. **Update the bot token and DB credentials**

Edit the following in `spam_guard_bot.py`:
```python
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
db = mysql.connector.connect(
    host="localhost",
    user="your_db_user",
    password="your_db_password",
    database="spam_guard"
)
```

4. **Initialize the database**

Run the SQL commands in `spam_guard.txt` using your MySQL client.

5. **Run the bot**

```bash
python spam_guard_bot.py
```

## 📊 Example Output

When spam is detected:
- Message is deleted.
- User is muted for 1 minute.
- Log is stored:
```
| username  | user_id | message           | action               | log_time           |
|-----------|---------|-------------------|----------------------|--------------------|
| johndoe   | 123456  | click here to win | Message deleted + User muted | 2025-06-25 12:45:02 |
```

## ✅ Advantages

- Real-time protection with automation
- Lightweight, easy deployment
- Reliable log storage with MySQL
- Doesn’t require a web server

## ⚠️ Limitations

- No web interface for viewing logs
- May flag false positives (e.g., marketing or promotional content)
- Keyword-based detection (no machine learning or NLP)

## 🏗️ Future Enhancements

- Web dashboard for admin access
- Integration with ML for smarter spam detection
- Notification system for alerts

## 👥 Contributors

- 22B01A0573
- 22B01A0586
- 22B01A05B3
- 23B05A0511  
Guided by: **Mr. P. Naga Raju**

## 📜 License

This project is open-source and free to use under the MIT License.
