#!/usr/bin/env python3
"""
Simple Astro AI Companion Runner
Personal Family Use Only
"""

import asyncio
import logging
import os
import sys
import threading
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.telegram_bot.bot_simple import SimpleAstroBot
from src.utils.config_simple import get_config
from loguru import logger

# Add Flask for web server
try:
    from flask import Flask
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    logger.warning("Flask not available, web server disabled")

# Configure logging
logger.add("logs/simple_astro.log", rotation="1 day", retention="7 days")

def create_web_server():
    """Create a simple Flask web server for Render."""
    if not FLASK_AVAILABLE:
        return None
    
    app = Flask(__name__)
    
    @app.route('/')
    def health_check():
        return {
            "status": "healthy",
            "service": "Astro AI Companion",
            "message": "Bot is running successfully!"
        }
    
    @app.route('/health')
    def health():
        return {"status": "ok"}
    
    return app

def run_web_server(app, port):
    """Run the web server in a separate thread."""
    if app:
        app.run(host='0.0.0.0', port=port, debug=False)

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

        # Create web server for Render
        web_app = create_web_server()
        port = int(os.environ.get('PORT', 8080))
        
        # Start web server in background thread
        if web_app:
            web_thread = threading.Thread(
                target=run_web_server, 
                args=(web_app, port),
                daemon=True
            )
            web_thread.start()
            logger.info(f"Web server started on port {port}")
            print(f"🌐 Web server started on port {port}")

        # Create and run bot
        bot = SimpleAstroBot()
        
        print("✅ Bot started successfully!")
        print("📱 Your personal astrology companion is now running...")
        print("💬 Chat with your bot on Telegram!")
        print(f"🌐 Health check available at: http://localhost:{port}/")

        # Use the synchronous run method for simple execution
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