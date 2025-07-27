#!/usr/bin/env python3
"""
Deployment Helper Script for Astro AI Companion
Helps prepare your project for GitHub and Render deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def check_git_installed():
    """Check if git is installed."""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_required_files():
    """Check if all required files exist."""
    required_files = [
        'run_simple.py',
        'requirements_simple.txt',
        'README.md',
        'env.example',
        'src/telegram_bot/bot_simple.py',
        'src/database/database.py',
        'src/utils/config.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    return missing_files

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main deployment helper function."""
    print("🚀 Astro AI Companion - Deployment Helper")
    print("=" * 50)
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first:")
        print("   Windows: https://git-scm.com/download/win")
        print("   Mac: brew install git")
        print("   Linux: sudo apt-get install git")
        return
    
    # Check required files
    missing_files = check_required_files()
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are present before deploying.")
        return
    
    print("✅ All required files found")
    
    # Initialize git repository
    if not Path('.git').exists():
        if not run_command('git init', 'Initializing Git repository'):
            return
    else:
        print("✅ Git repository already exists")
    
    # Add all files
    if not run_command('git add .', 'Adding files to Git'):
        return
    
    # Check if there are changes to commit
    result = subprocess.run('git status --porcelain', shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("✅ No changes to commit")
    else:
        # Commit changes
        if not run_command('git commit -m "Initial commit: Clean Astro AI Companion"', 'Committing changes'):
            return
    
    print("\n🎯 NEXT STEPS:")
    print("1. Create a GitHub repository:")
    print("   - Go to https://github.com")
    print("   - Click 'New repository'")
    print("   - Name it 'astro-ai-companion'")
    print("   - Make it Public")
    print("   - Don't initialize with README (we already have one)")
    
    print("\n2. Connect to GitHub:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/astro-ai-companion.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n3. Deploy to Render:")
    print("   - Go to https://render.com")
    print("   - Sign up with GitHub")
    print("   - Click 'New Web Service'")
    print("   - Connect your repository")
    print("   - Set environment variables:")
    print("     * TELEGRAM_BOT_TOKEN = your_bot_token")
    print("     * ENVIRONMENT = production")
    print("     * DEBUG = false")
    print("   - Build Command: pip install -r requirements_simple.txt")
    print("   - Start Command: python run_simple.py")
    
    print("\n📋 IMPORTANT REMINDERS:")
    print("✅ Make sure your repository is PUBLIC (Render needs access)")
    print("✅ Get your Telegram bot token from @BotFather")
    print("✅ Test your bot after deployment")
    print("✅ Check Render logs if there are issues")
    
    print("\n🌟 Your Astro AI Companion will be running 24/7 for FREE!")
    print("📱 Access it from anywhere via Telegram")
    print("🔄 Auto-updates when you push to GitHub")

if __name__ == "__main__":
    main() 