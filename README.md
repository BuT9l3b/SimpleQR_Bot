# SimpleQR Telegram Bot

A Telegram bot that can generate and decode QR codes. The bot supports both regular chat mode and inline mode.

## Features

- Generate QR codes from text or links
- Decode QR codes from images
- Inline mode support
- Logging system for error tracking
- Configuration via environment variables


## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BuT9l3b/SimpleQR_Bot.git
cd SimpleQR_Bot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=your_bot_username_here
STORAGE_CHANNEL=your_storage_channel_id_here
```

## Usage

1. Start the bot:
```bash
python -m app.main
```

2. In Telegram:
   - Send any text or link to generate a QR code
   - Send an image with a QR code to decode it
   - Use inline mode by typing `@your_bot_username` in any chat

## Commands

- `/start` - Start the bot
- `/help` - Show help message


## License

This project is licensed under the MIT License - see the LICENSE file for details.