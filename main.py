import os
import sys
import threading
import time
import random
import subprocess

# Check for help flag
if len(sys.argv) > 1 and any(arg in ["--help", "-h", "/?"] for arg in sys.argv):
    print("\nKeep Awake Utility (GUI Version) - Command Line Usage")
    print("=================================================")
    print("Options:")
    print("  --help, -h               Show this help message")
    print("  --auto-start, -a         Automatically start the utility")
    print("  --max-timer, -m          Use maximum timer (10 hours)")
    print("  --timer=HOURS            Set specific timer hours (1, 2, 5, or 10)")
    sys.exit(0)

# Import dependencies
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    import pyautogui
    import psutil
    from PIL import Image, ImageDraw
except ImportError as e:
    print(f"Missing required packages: {str(e)}")
    sys.exit(1)

# Check for tray support
try:
    import pystray
    from pystray import MenuItem as Item
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False

class KeepAwakeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keep Awake Utility")
        self.root.geometry("740x560")
        self.root.minsize(740, 560)
        self.root.resizable(False, False)

        # State
        self.active = False
        self.timer_active = False
        self.shutdown_scheduled = False
        self.remaining_time = 0

        # Threads
        self.activity_thread = None
        self.timer_thread = None
        self.shutdown_thread = None
        self.tray_thread = None
        self.stop_threads = threading.Event()

        self.status_text = tk.StringVar(value="Inactive")
        self.timer_text = tk.StringVar(value="No shutdown scheduled")

        self.setup_gui()

        if HAS_TRAY:
            self.setup_tray_icon()

        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def setup_gui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(frame, text="Keep Awake Utility", font=("Helvetica", 18, "bold"))
        title.pack(pady=(0, 15))

        # Timer controls
        timer_frame = ttk.LabelFrame(frame, text="Shutdown Timer", padding=10)
        timer_frame.pack(fill=tk.X, pady=(0, 10))

        self.timer_options = ["Never", "1 hour", "2 hours", "5 hours", "10 hours"]
        self.timer_var = tk.StringVar(value="Never")

        ttk.Label(timer_frame, text="Shutdown after:").pack(side=tk.LEFT)
        timer_menu = ttk.Combobox(timer_frame, textvariable=self.timer_var, values=self.timer_options, state="readonly", width=12)
        timer_menu.pack(side=tk.LEFT, padx=10)
        timer_menu.bind("<<ComboboxSelected>>", self.on_timer_change)

        # Status area
        status_frame = ttk.LabelFrame(frame, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(status_frame, text="Current state:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(status_frame, textvariable=self.status_text).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(status_frame, text="Shutdown timer:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(status_frame, textvariable=self.timer_text).grid(row=1, column=1, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(15, 10))

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_keep_awake)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_keep_awake, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save", command=self.update_status)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Cancel Shutdown", command=self.cancel_shutdown, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        footer = ttk.Label(frame, text="Simulates mouse/keyboard activity to keep your PC awake.")
        footer.pack(pady=(10, 5))

    def on_timer_change(self, event=None):
        if self.active:
            self.apply_timer_setting()

    def apply_timer_setting(self):
        option = self.timer_var.get()
        hours_map = {"1 hour": 1, "2 hours": 2, "5 hours": 5, "10 hours": 10}
        self.timer_active = False

        if option == "Never":
            self.timer_text.set("No shutdown scheduled")
            self.cancel_button.config(state=tk.DISABLED)
            return

        if option in hours_map:
            self.remaining_time = hours_map[option] * 3600
            self.timer_active = True
            self.cancel_button.config(state=tk.NORMAL)
            self.timer_thread = threading.Thread(target=self.countdown_timer, daemon=True)
            self.timer_thread.start()

    def start_keep_awake(self):
        if self.active:
            return
        self.active = True
        self.status_text.set("Active")
        self.stop_threads.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.apply_timer_setting()
        self.activity_thread = threading.Thread(target=self.simulate_activity, daemon=True)
        self.activity_thread.start()
        self.update_tray_icon()

    def stop_keep_awake(self):
        self.active = False
        self.status_text.set("Inactive")
        self.timer_text.set("No shutdown scheduled")
        self.stop_threads.set()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        self.timer_active = False
        self.shutdown_scheduled = False
        self.update_tray_icon()

    def simulate_activity(self):
        while not self.stop_threads.is_set():
            try:
                if random.choice([True, False]):
                    x, y = pyautogui.position()
                    pyautogui.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=0.1)
                else:
                    pyautogui.press('shift')
                time.sleep(6)
            except Exception as e:
                messagebox.showerror("Simulation Error", str(e))
                self.stop_keep_awake()
                break

    def countdown_timer(self):
        while self.timer_active and self.remaining_time > 0 and not self.stop_threads.is_set():
            mins, secs = divmod(self.remaining_time, 60)
            hrs, mins = divmod(mins, 60)
            formatted = f"{hrs:02}:{mins:02}:{secs:02}"
            self.root.after(0, self.timer_text.set, f"Shutdown in {formatted}")
            time.sleep(1)
            self.remaining_time -= 1

        if self.timer_active and not self.stop_threads.is_set():
            self.root.after(0, self.schedule_shutdown)

    def schedule_shutdown(self):
        self.shutdown_scheduled = True
        messagebox.showwarning("Shutdown", "Your PC will shut down in 1 minute.")
        self.shutdown_thread = threading.Thread(target=self.execute_shutdown, daemon=True)
        self.shutdown_thread.start()

    def execute_shutdown(self):
        for _ in range(60):
            if not self.shutdown_scheduled or self.stop_threads.is_set():
                return
            time.sleep(1)
        try:
            if sys.platform == 'win32':
                subprocess.run(['shutdown', '/s', '/t', '0'])
            else:
                subprocess.run(['shutdown', '-h', 'now'])
        except Exception as e:
            messagebox.showerror("Shutdown Error", str(e))

    def cancel_shutdown(self):
        self.shutdown_scheduled = False
        self.timer_active = False
        self.timer_text.set("Shutdown cancelled")
        self.cancel_button.config(state=tk.DISABLED)
        try:
            if sys.platform == 'win32':
                subprocess.run(['shutdown', '/a'])
        except Exception as e:
            messagebox.showerror("Cancel Error", str(e))

    def update_status(self):
        self.status_text.set("Active" if self.active else "Inactive")
        if self.timer_active:
            mins, secs = divmod(self.remaining_time, 60)
            hrs, mins = divmod(mins, 60)
            self.timer_text.set(f"Shutdown in {hrs:02}:{mins:02}:{secs:02}")
        else:
            self.timer_text.set("No shutdown scheduled")
        self.update_tray_tooltip()
        self.update_tray_icon()

    def minimize_to_tray(self):
        self.root.withdraw()

    def restore_from_tray(self):
        self.root.deiconify()
        self.root.lift()

    def setup_tray_icon(self):
        self.icon = pystray.Icon("keepawake", self.get_icon_image(), "Keep Awake Utility", menu=pystray.Menu(
            Item("Show", self.restore_from_tray),
            Item("Start", self.start_keep_awake),
            Item("Stop", self.stop_keep_awake),
            Item("Exit", self.exit_app)
        ))

        self.tray_thread = threading.Thread(target=self.icon.run, daemon=True)
        self.tray_thread.start()

        self.tooltip_updater = threading.Thread(target=self.tray_tooltip_loop, daemon=True)
        self.tooltip_updater.start()

    def tray_tooltip_loop(self):
        while True:
            time.sleep(5)
            self.update_tray_tooltip()
            self.update_tray_icon()

    def update_tray_tooltip(self):
        if HAS_TRAY and hasattr(self, "icon"):
            tooltip = f"Status: {self.status_text.get()} | {self.timer_text.get()}"
            self.icon.title = tooltip

    def update_tray_icon(self):
        if not HAS_TRAY or not hasattr(self, "icon"):
            return
        self.icon.icon = self.get_icon_image()

    def get_icon_image(self):
        try:
            icon_path = "awake_icon.png" if self.active else "sleep_icon.png"
            if not os.path.exists(icon_path):
                icon_path = "generated-icon.png"
            return Image.open(icon_path)
        except Exception:
            return Image.new('RGB', (64, 64), color=(128, 128, 128))

    def exit_app(self):
        self.stop_keep_awake()
        if HAS_TRAY and hasattr(self, "icon"):
            self.icon.stop()
        self.root.quit()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = KeepAwakeApp(root)

    auto_start = "--auto-start" in sys.argv or "-a" in sys.argv
    if auto_start:
        max_timer = "--max-timer" in sys.argv or "-m" in sys.argv
        for arg in sys.argv:
            if arg.startswith("--timer="):
                try:
                    hrs = int(arg.split("=")[1])
                    if hrs in [1, 2, 5, 10]:
                        app.timer_var.set(f"{hrs} hour" if hrs == 1 else f"{hrs} hours")
                except:
                    pass
        if max_timer:
            app.timer_var.set("10 hours")
        root.after(1000, app.start_keep_awake)

    root.after(500, root.iconify)
    root.mainloop()

if __name__ == "__main__":
    main()
