#!/usr/bin/env python3
"""
Stop Bot Process Script
Use this to stop any running bot instances before deployment
"""

import os
import subprocess
import sys

def stop_python_processes():
    """Stop any running Python processes that might be the bot."""
    try:
        # For Windows
        if os.name == 'nt':
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                  capture_output=True, text=True)
            if 'python.exe' in result.stdout:
                print("🛑 Stopping Python processes...")
                subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                             capture_output=True)
                print("✅ Python processes stopped")
            else:
                print("ℹ️ No Python processes found")
        
        # For Unix/Linux
        else:
            result = subprocess.run(['pgrep', '-f', 'python'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("🛑 Stopping Python processes...")
                subprocess.run(['pkill', '-f', 'python'], 
                             capture_output=True)
                print("✅ Python processes stopped")
            else:
                print("ℹ️ No Python processes found")
                
    except Exception as e:
        print(f"⚠️ Error stopping processes: {e}")

def main():
    """Main function."""
    print("🛑 Bot Process Stopper")
    print("=" * 30)
    
    stop_python_processes()
    
    print("\n✅ Ready for deployment!")
    print("💡 Now you can deploy to Render without conflicts")

if __name__ == "__main__":
    main() 