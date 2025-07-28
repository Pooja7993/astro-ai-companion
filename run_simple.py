#!/usr/bin/env python3
"""
Simple Astro AI Companion Runner
Personal Family Use Only
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.telegram_bot.bot_simple import SimpleAstroBot
from src.utils.config_simple import get_config
from loguru import logger

# Configure logging
logger.add("logs/simple_astro.log", rotation="1 day", retention="7 days")

def main():
    """Main function to run the simple Astro AI Companion."""
    try:
        # Load configuration
        config = get_config()

        # Check for required environment variables
        if not config.has_telegram_token():
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            print("❌ Error: TELEGRAM_BOT_TOKEN not found!")
            print("Please set your Telegram bot token in the environment variables.")
            print("For local testing, create a .env file with:")
            print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
            print("TELEGRAM_CHAT_ID=5929651379")
            return

        logger.info("Starting Simple Astro AI Companion...")
        print("🌟 Starting Simple Astro AI Companion...")

        # Create and run bot
        bot = SimpleAstroBot()

        # Run the bot
        print("✅ Bot started successfully!")
        print("📱 Your personal astrology companion is now running...")
        print("💬 Chat with your bot on Telegram!")

        bot.run_sync()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        print(f"❌ Error running bot: {e}")
        print("Please check your environment variables and try again.")

if __name__ == "__main__":
    main() 