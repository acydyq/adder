#!/usr/bin/env python3
"""
Helper script to automatically start the Keep Awake utility 
with the maximum timer setting (10 hours).
"""

import sys
import os
import time
import subprocess
import threading
import signal

def run_auto_commands(app_type):
    """Wait for app to start and then send commands to set timer and start"""
    # Wait for app to initialize
    time.sleep(2)
    
    if app_type == "console":
        # For console app, we need to input commands
        # Start with timer command
        print("timer")
        # Select max timer (option 4 - 10 hours)
        time.sleep(1)
        print("4")
        # Start the keep awake function
        time.sleep(1)
        print("start")
    else:
        # For GUI app, we'd use a different approach
        # This is handled in the main.py with command-line arguments
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_with_max_timer.py [app_script.py]")
        sys.exit(1)
        
    target_script = sys.argv[1]
    
    # Determine if this is console or GUI version
    app_type = "console" if "console" in target_script else "gui"
    
    if app_type == "console":
        # For console app, use threading to simulate user input
        command_thread = threading.Thread(target=run_auto_commands, args=(app_type,))
        command_thread.daemon = True
        command_thread.start()
        
        # Start the app and redirect its stdin to this process
        os.system(f"python {target_script}")
    else:
        # For GUI app, pass command-line arguments
        subprocess.Popen(["python", target_script, "--auto-start", "--timer=10"])
        
if __name__ == "__main__":
    main()