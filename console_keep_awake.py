#!/usr/bin/env python3
"""
Console-based Keep Awake Utility
This script simulates activity to prevent a computer from sleeping,
with an optional automatic shutdown timer.
"""

import os
import sys
import threading
import time
import random
import subprocess
from datetime import datetime, timedelta

class KeepAwakeConsoleApp:
    def __init__(self):
        # Initialize state variables
        self.active = False
        self.timer_active = False
        self.shutdown_scheduled = False
        self.remaining_time = 0
        self.activity_thread = None
        self.timer_thread = None
        self.shutdown_thread = None
        self.stop_threads = threading.Event()
        self.timer_options = ["Never", "1 hour", "2 hours", "5 hours", "10 hours"]
        self.current_timer = self.timer_options[0]
        
        # For demonstration purposes in Replit
        self.simulation_log = []
        
        # Welcome message
        self.print_welcome()
    
    def print_welcome(self):
        """Print welcome message and instructions"""
        print("\n" + "=" * 50)
        print(" " * 15 + "KEEP AWAKE UTILITY")
        print("=" * 50)
        print("This utility prevents your PC from sleeping by simulating activity.")
        print("When the timer expires, your PC will automatically shut down.")
        print("\nCommands:")
        print("  start - Start keeping the PC awake")
        print("  stop  - Stop the utility")
        print("  timer - Set shutdown timer")
        print("  status - Show current status")
        print("  exit  - Exit the application")
        print("=" * 50 + "\n")
    
    def print_status(self):
        """Print current status"""
        status = "Active" if self.active else "Inactive"
        
        if self.timer_active:
            hours, remainder = divmod(self.remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            timer_status = f"Shutdown in {time_str}"
        else:
            timer_status = "No shutdown scheduled"
        
        print(f"\nCurrent state: {status}")
        print(f"Shutdown timer: {timer_status}")
        
        if self.active and len(self.simulation_log) > 0:
            print("\nRecent activity simulation:")
            for log in self.simulation_log[-5:]:  # Show last 5 log entries
                print(f"  - {log}")
        print()
    
    def simulate_activity(self):
        """Thread function to simulate mouse/keyboard activity"""
        while not self.stop_threads.is_set():
            try:
                # In a real environment, this would use pyautogui to move the mouse or press keys
                # For Replit, we just simulate by logging what would happen
                
                # Alternate between simulated mouse movement and key press
                current_time = datetime.now().strftime("%H:%M:%S")
                
                if random.choice([True, False]):
                    # Simulate small mouse movement
                    x_move = random.randint(-5, 5)
                    y_move = random.randint(-5, 5)
                    self.simulation_log.append(f"[{current_time}] Mouse moved by ({x_move}, {y_move}) pixels")
                else:
                    # Simulate key press
                    self.simulation_log.append(f"[{current_time}] Pressed 'Shift' key")
                
                # Keep log from growing too large
                if len(self.simulation_log) > 100:
                    self.simulation_log = self.simulation_log[-50:]
                
                # Wait before next activity simulation (6 seconds)
                for _ in range(30):  # 30 * 0.2 = 6 seconds
                    if self.stop_threads.is_set():
                        break
                    time.sleep(0.2)
                    
            except Exception as e:
                print(f"Error in activity simulation: {str(e)}")
                self.stop_keep_awake()
                break
    
    def start_keep_awake(self):
        """Start the keep awake functionality"""
        if self.active:
            print("Already active!")
            return
            
        self.active = True
        self.stop_threads.clear()
        
        print("Starting keep awake functionality...")
        
        # Start activity simulation thread
        self.activity_thread = threading.Thread(target=self.simulate_activity, daemon=True)
        self.activity_thread.start()
        
        # Check if timer is set
        self.check_timer_selection()
        print("Keep awake functionality started successfully.")
    
    def stop_keep_awake(self):
        """Stop the keep awake functionality"""
        if not self.active:
            print("Not currently active!")
            return
        
        # Signal threads to stop
        self.stop_threads.set()
        
        # Update state
        self.active = False
        print("Stopped keep awake functionality.")
        
        # Reset timer if active
        if self.timer_active:
            self.timer_active = False
            self.current_timer = self.timer_options[0]
            print("Timer reset.")
    
    def show_timer_options(self):
        """Show and prompt for timer selection"""
        print("\nShutdown Timer Options:")
        for i, option in enumerate(self.timer_options):
            print(f"{i+1}. {option}")
        
        try:
            choice = input("\nSelect a timer option (1-5): ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.timer_options):
                self.current_timer = self.timer_options[int(choice)-1]
                print(f"Timer set to: {self.current_timer}")
                
                if self.active:
                    self.check_timer_selection()
                    
            else:
                print("Invalid selection. Please choose a number between 1 and 5.")
        except Exception as e:
            print(f"Error setting timer: {str(e)}")
    
    def check_timer_selection(self):
        """Check and apply the selected timer setting"""
        selection = self.current_timer
        
        # Cancel any existing timer
        self.timer_active = False
        self.shutdown_scheduled = False
        
        if selection == "Never":
            print("No shutdown scheduled.")
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
            print(f"Shutdown scheduled in {selection}.")
            
            # Start timer thread
            self.timer_thread = threading.Thread(target=self.countdown_timer, daemon=True)
            self.timer_thread.start()
    
    def countdown_timer(self):
        """Thread function for countdown timer"""
        while self.timer_active and not self.stop_threads.is_set() and self.remaining_time > 0:
            # In a real application this would update UI - here we just decrement
            time.sleep(1)
            self.remaining_time -= 1
        
        # If timer completed and wasn't cancelled, initiate shutdown
        if self.timer_active and self.remaining_time <= 0 and not self.stop_threads.is_set():
            print("Timer expired! Initiating shutdown...")
            self.schedule_shutdown()
    
    def schedule_shutdown(self):
        """Schedule system shutdown"""
        self.shutdown_scheduled = True
        
        print("\n" + "!" * 60)
        print("! WARNING: Your PC will shut down in 1 minute due to timer expiration !")
        print("! Type 'cancel' to abort the shutdown                              !")
        print("!" * 60 + "\n")
        
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
            print("Executing shutdown command...")
            try:
                if sys.platform == 'win32':
                    # Windows shutdown command
                    print("SIMULATED: shutdown /s /t 0")
                    # subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
                else:
                    # Linux/macOS shutdown command
                    print("SIMULATED: shutdown -h now")
                    # subprocess.run(['shutdown', '-h', 'now'], check=True)
                print("Shutdown command would be executed now in a real environment.")
            except Exception as e:
                print(f"Error: Failed to shutdown: {str(e)}")
    
    def cancel_shutdown(self):
        """Cancel scheduled shutdown"""
        if self.shutdown_scheduled:
            self.shutdown_scheduled = False
            print("Shutdown cancelled.")
            try:
                if sys.platform == 'win32':
                    # Windows abort shutdown command
                    print("SIMULATED: shutdown /a")
                    # subprocess.run(['shutdown', '/a'], check=True)
            except Exception as e:
                print(f"Error: Failed to cancel shutdown: {str(e)}")
        
        # Reset timer
        self.timer_active = False
        self.current_timer = self.timer_options[0]

    def advanced_features(self):
        """Show advanced features menu"""
        print("\nAdvanced Features:")
        print("1. System Resource Monitor")
        print("2. Custom Activity Pattern")
        print("3. Schedule Start/Stop Times")
        print("4. Power Usage Analysis")
        print("5. Back to main menu")
        
        try:
            choice = input("\nSelect an option (1-5): ")
            if choice == "1":
                self.show_resource_monitor()
            elif choice == "2":
                self.custom_activity_pattern()
            elif choice == "3":
                self.schedule_operation()
            elif choice == "4":
                self.power_usage_analysis()
            elif choice == "5":
                return
            else:
                print("Invalid option. Please choose a number between 1 and 5.")
        except Exception as e:
            print(f"Error in advanced features: {str(e)}")
    
    def show_resource_monitor(self):
        """Display system resource usage"""
        try:
            import psutil
            
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            
            # Memory information
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk information
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            print("\nSystem Resource Monitor:")
            print(f"CPU Usage: {cpu_percent}%")
            if cpu_freq:
                print(f"CPU Frequency: {cpu_freq.current:.2f} MHz")
            print(f"Memory Usage: {memory_percent}%")
            print(f"Disk Usage: {disk_percent}%")
            
            # Battery information if available
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    print(f"Battery: {battery.percent}%")
                    if battery.power_plugged:
                        print("Power: Plugged In")
                    else:
                        secs_left = battery.secsleft
                        if secs_left != psutil.POWER_TIME_UNLIMITED:
                            hours, remainder = divmod(secs_left, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print(f"Battery Time Left: {hours:02d}:{minutes:02d}:{seconds:02d}")
                        else:
                            print("Battery Time Left: Unlimited")
            
        except ImportError:
            print("Resource monitoring requires psutil module.")
        except Exception as e:
            print(f"Error reading system resources: {str(e)}")
    
    def custom_activity_pattern(self):
        """Configure custom activity pattern"""
        print("\nCustom Activity Pattern:")
        print("Configure how the utility simulates activity")
        
        print("\nActivity Types:")
        print("1. Mouse movement only")
        print("2. Keyboard only")
        print("3. Both mouse and keyboard (default)")
        
        print("\nActivity Frequency:")
        print("1. Low (every 30 seconds)")
        print("2. Medium (every 10 seconds, default)")
        print("3. High (every 3 seconds)")
        
        print("\nThis would allow custom configuration of activity patterns in a real implementation.")
        input("\nPress Enter to return to advanced features...")
    
    def schedule_operation(self):
        """Schedule automatic start/stop times"""
        print("\nSchedule Operation:")
        print("Configure automatic start and stop times for the utility")
        
        print("\nThis feature would allow scheduling when the utility")
        print("automatically starts and stops based on time of day.")
        print("For example, automatically running during work hours")
        print("or stopping during specific maintenance windows.")
        
        input("\nPress Enter to return to advanced features...")
    
    def power_usage_analysis(self):
        """Show power usage analysis"""
        print("\nPower Usage Analysis:")
        print("Analysis of system power consumption and recommendations")
        
        print("\nA real implementation would monitor power usage patterns")
        print("and provide recommendations to optimize battery life")
        print("or reduce electricity consumption.")
        
        print("\nPower-saving recommendations would include:")
        print("- Screen brightness adjustments")
        print("- Sleep settings for unused peripherals")
        print("- Background app power consumption analysis")
        
        input("\nPress Enter to return to advanced features...")
    
    def run_interactive(self):
        """Run the application in interactive command mode"""
        running = True
        
        while running:
            try:
                command = input("\nEnter command (start/stop/timer/status/advanced/exit): ").strip().lower()
                
                if command == 'start':
                    self.start_keep_awake()
                elif command == 'stop':
                    self.stop_keep_awake()
                elif command == 'timer':
                    self.show_timer_options()
                elif command == 'status':
                    self.print_status()
                elif command == 'advanced':
                    self.advanced_features()
                elif command == 'cancel':
                    self.cancel_shutdown()
                elif command == 'exit':
                    if self.active:
                        confirm = input("Keep awake is still active. Are you sure you want to exit? (y/n): ").lower()
                        if confirm == 'y':
                            self.stop_keep_awake()
                            running = False
                    else:
                        running = False
                else:
                    print("Unknown command. Available commands: start, stop, timer, status, advanced, exit")
            
            except KeyboardInterrupt:
                print("\nReceived interrupt signal.")
                self.stop_keep_awake()
                running = False
            except Exception as e:
                print(f"Error: {str(e)}")
        
        print("Exiting Keep Awake Utility. Goodbye!")

def main():
    app = KeepAwakeConsoleApp()
    app.run_interactive()

if __name__ == "__main__":
    main()