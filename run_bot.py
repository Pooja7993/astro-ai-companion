#!/usr/bin/env python3
"""
Run Telegram Bot for Render Deployment
"""

import os
import asyncio
from src.telegram_bot.family_bot import FamilyTelegramBot

def main():
    """Main function to run the Telegram bot."""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable is required")
        return
    
    print("🤖 Starting Family Telegram Bot...")
    bot = FamilyTelegramBot(token)
    bot.run()

if __name__ == "__main__":
    main()