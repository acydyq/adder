# No GUI imports for compatibility with headless environments
# import tkinter as tk
# from tkinter import ttk, messagebox
# import pyautogui
import os
import sys
import threading
import time
import psutil
import pystray
from PIL import Image, ImageDraw
import subprocess
import random

class KeepAwakeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keep Awake Utility")
        self.root.geometry("400x300")
        self.root.minsize(400, 300)
        self.root.resizable(False, False)
        
        # Set app icon (Windows specific)
        if sys.platform == 'win32':
            self.root.iconbitmap(default='')
        
        # Initialize state variables
        self.active = False
        self.timer_active = False
        self.shutdown_scheduled = False
        self.remaining_time = 0
        self.activity_thread = None
        self.timer_thread = None
        self.shutdown_thread = None
        self.stop_threads = threading.Event()
        
        # Setup GUI
        self.setup_gui()
        
        # Configure window close behavior
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
        # Create system tray icon
        self.setup_system_tray()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Keep Awake Utility", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Timer selection frame
        timer_frame = ttk.LabelFrame(main_frame, text="Shutdown Timer", padding="10")
        timer_frame.pack(fill=tk.X, pady=10)
        
        # Timer dropdown
        ttk.Label(timer_frame, text="Shutdown after:").pack(side=tk.LEFT, padx=(0, 10))
        self.timer_options = ["Never", "1 hour", "2 hours", "5 hours", "10 hours"]
        self.timer_var = tk.StringVar(value=self.timer_options[0])
        timer_dropdown = ttk.Combobox(timer_frame, textvariable=self.timer_var, values=self.timer_options, state="readonly", width=10)
        timer_dropdown.pack(side=tk.LEFT)
        timer_dropdown.bind("<<ComboboxSelected>>", self.on_timer_change)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        # Status info
        self.status_text = tk.StringVar(value="Inactive")
        self.timer_text = tk.StringVar(value="No shutdown scheduled")
        
        status_label = ttk.Label(status_frame, text="Current state:")
        status_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.status_value = ttk.Label(status_frame, textvariable=self.status_text, font=("Helvetica", 10, "bold"))
        self.status_value.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        timer_label = ttk.Label(status_frame, text="Shutdown timer:")
        timer_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.timer_value = ttk.Label(status_frame, textvariable=self.timer_text)
        self.timer_value.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=20)
        
        # Start/Stop buttons
        self.start_button = ttk.Button(controls_frame, text="Start Keep Awake", command=self.start_keep_awake)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(controls_frame, text="Stop", command=self.stop_keep_awake, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Cancel shutdown button
        self.cancel_button = ttk.Button(controls_frame, text="Cancel Shutdown", command=self.cancel_shutdown, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.RIGHT)
        
        # Info text
        info_text = (
            "This utility prevents your PC from sleeping by simulating activity.\n"
            "When the timer expires, your PC will automatically shut down.\n"
            "You can minimize this window to the system tray."
        )
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.CENTER, wraplength=350)
        info_label.pack(side=tk.BOTTOM, pady=10)

    def start_keep_awake(self):
        """Start the keep awake functionality"""
        if self.active:
            return
            
        self.active = True
        self.stop_threads.clear()
        
        # Update UI
        self.status_text.set("Active")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start activity simulation thread
        self.activity_thread = threading.Thread(target=self.simulate_activity, daemon=True)
        self.activity_thread.start()
        
        # Check if timer is set
        self.check_timer_selection()
    
    def stop_keep_awake(self):
        """Stop the keep awake functionality"""
        if not self.active:
            return
        
        # Signal threads to stop
        self.stop_threads.set()
        
        # Update UI
        self.active = False
        self.status_text.set("Inactive")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Reset timer if active
        if self.timer_active:
            self.timer_active = False
            self.timer_text.set("No shutdown scheduled")
            self.cancel_button.config(state=tk.DISABLED)
    
    def simulate_activity(self):
        """Thread function to simulate mouse/keyboard activity"""
        while not self.stop_threads.is_set():
            try:
                # Get current screen size
                screen_width, screen_height = pyautogui.size()
                
                # Alternate between mouse movement and key press
                if random.choice([True, False]):
                    # Small mouse movement to not disturb user
                    current_x, current_y = pyautogui.position()
                    new_x = max(0, min(screen_width, current_x + random.randint(-5, 5)))
                    new_y = max(0, min(screen_height, current_y + random.randint(-5, 5)))
                    pyautogui.moveTo(new_x, new_y, duration=0.1)
                else:
                    # Press and release a harmless key like shift
                    pyautogui.press('shift')
                
                # Wait before next activity simulation
                # Sleep in small increments to respond to stop signals faster
                for _ in range(30):  # 30 * 0.2 = 6 seconds
                    if self.stop_threads.is_set():
                        break
                    time.sleep(0.2)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Activity simulation error: {str(e)}")
                self.stop_keep_awake()
                break
    
    def on_timer_change(self, event=None):
        """Handle timer dropdown selection change"""
        if self.active:
            self.check_timer_selection()
    
    def check_timer_selection(self):
        """Check and apply the selected timer setting"""
        selection = self.timer_var.get()
        
        # Cancel any existing timer
        self.timer_active = False
        self.shutdown_scheduled = False
        
        if selection == "Never":
            self.timer_text.set("No shutdown scheduled")
            self.cancel_button.config(state=tk.DISABLED)
            return
        
        # Map selection to hours
        hours_map = {
            "1 hour": 1,
            "2 hours": 2,
            "5 hours": 5,
            "10 hours": 10
        }
        
        if selection in hours_map:
            hours = hours_map[selection]
            self.remaining_time = hours * 3600  # Convert hours to seconds
            self.timer_active = True
            self.timer_text.set(f"Shutdown in {selection}")
            self.cancel_button.config(state=tk.NORMAL)
            
            # Start timer thread
            self.timer_thread = threading.Thread(target=self.countdown_timer, daemon=True)
            self.timer_thread.start()
    
    def countdown_timer(self):
        """Thread function for countdown timer"""
        while self.timer_active and not self.stop_threads.is_set() and self.remaining_time > 0:
            # Format time as HH:MM:SS
            hours, remainder = divmod(self.remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Update timer display
            self.timer_text.set(f"Shutdown in {time_str}")
            
            # Wait one second
            time.sleep(1)
            self.remaining_time -= 1
        
        # If timer completed and wasn't cancelled, initiate shutdown
        if self.timer_active and self.remaining_time <= 0 and not self.stop_threads.is_set():
            self.timer_text.set("Initiating shutdown...")
            self.schedule_shutdown()
    
    def schedule_shutdown(self):
        """Schedule system shutdown"""
        self.shutdown_scheduled = True
        
        # Show warning notification
        messagebox.showwarning(
            "Shutdown Scheduled", 
            "Your PC will shut down in 1 minute due to the timer expiration.\n"
            "Click 'Cancel Shutdown' to abort."
        )
        
        # Start shutdown thread
        self.shutdown_thread = threading.Thread(target=self.execute_shutdown, daemon=True)
        self.shutdown_thread.start()
    
    def execute_shutdown(self):
        """Execute system shutdown after a short delay"""
        # Wait 60 seconds before shutdown to give user time to cancel
        for i in range(60):
            if not self.shutdown_scheduled or self.stop_threads.is_set():
                return
            time.sleep(1)
        
        if self.shutdown_scheduled:
            try:
                if sys.platform == 'win32':
                    # Windows shutdown command
                    subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
                else:
                    # Linux/macOS shutdown command
                    subprocess.run(['shutdown', '-h', 'now'], check=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to shutdown: {str(e)}")
                self.timer_text.set("Shutdown failed")
    
    def cancel_shutdown(self):
        """Cancel scheduled shutdown"""
        if self.shutdown_scheduled:
            self.shutdown_scheduled = False
            self.timer_text.set("Shutdown cancelled")
            try:
                if sys.platform == 'win32':
                    # Windows abort shutdown command
                    subprocess.run(['shutdown', '/a'], check=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel shutdown: {str(e)}")
        
        # Reset timer
        self.timer_active = False
        self.timer_var.set("Never")
        self.cancel_button.config(state=tk.DISABLED)
    
    def create_tray_icon(self):
        """Create a system tray icon image"""
        # Create a blank image
        image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a simple icon (a filled circle)
        draw.ellipse((5, 5, 59, 59), fill=(0, 128, 255))
        
        return image
    
    def setup_system_tray(self):
        """Set up the system tray icon and menu"""
        image = self.create_tray_icon()
        
        menu = (
            pystray.MenuItem('Show', self.show_window),
            pystray.MenuItem('Start Keep Awake', self.start_from_tray),
            pystray.MenuItem('Stop Keep Awake', self.stop_from_tray),
            pystray.MenuItem('Exit', self.exit_app)
        )
        
        self.icon = pystray.Icon("keep_awake", image, "Keep Awake Utility", menu)
        
        # Start icon in a separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def minimize_to_tray(self):
        """Minimize the application to system tray"""
        self.root.withdraw()  # Hide the window
    
    def show_window(self):
        """Show the main window from the system tray"""
        self.root.deiconify()  # Show the window
        self.root.lift()  # Bring to front
    
    def start_from_tray(self):
        """Start keep awake functionality from the system tray"""
        self.show_window()
        self.start_keep_awake()
    
    def stop_from_tray(self):
        """Stop keep awake functionality from the system tray"""
        self.stop_keep_awake()
    
    def exit_app(self):
        """Exit the application completely"""
        # Stop any running activities
        self.stop_keep_awake()
        
        # Cancel shutdown if scheduled
        if self.shutdown_scheduled:
            self.cancel_shutdown()
        
        # Stop the tray icon
        self.icon.stop()
        
        # Destroy the main window
        self.root.destroy()
        
        # Exit the application
        sys.exit(0)

def main():
    root = tk.Tk()
    app = KeepAwakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    # Try to use a more modern style if available
    try:
        from tkinter import ttk
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'winnative' in available_themes:
            style.theme_use('winnative')
        elif 'clam' in available_themes:
            style.theme_use('clam')
    except Exception:
        pass  # Fall back to default style
    
    main()
