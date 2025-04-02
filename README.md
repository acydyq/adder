# Keep Awake Utility

A utility that keeps your Windows PC awake by simulating mouse movements and keyboard activity, with an optional automatic shutdown timer.

## Features

- **Activity Simulation**: Prevents your PC from sleeping by simulating mouse movements and keyboard presses at regular intervals
- **Shutdown Timer**: Set a timer (1, 2, 5, or 10 hours) after which your PC will automatically shut down
- **System Resource Monitor**: View real-time CPU, memory, disk, and battery usage information
- **Custom Activity Patterns**: Configure how the utility simulates activity (mouse, keyboard, or both)
- **Command-line Interface**: Easy-to-use console interface for controlling the application

## Installation

1. Ensure you have Python 3.6+ installed on your system
2. Install required dependencies:
   ```
   pip install psutil pillow
   ```
3. In a Windows environment with a GUI, also install:
   ```
   pip install pyautogui pystray
   ```

## Usage

### Console Version (Works in all environments)

Run the console-based version of the application:

```
python console_keep_awake.py
```

Follow the on-screen instructions to control the application:
- `start` - Start keeping your PC awake
- `stop` - Stop the utility
- `timer` - Set a shutdown timer
- `status` - Check the current status
- `advanced` - Access advanced features
- `exit` - Exit the application

### GUI Version (Windows only)

In a Windows environment, you can also run the GUI version which includes system tray functionality:

```
python main.py
```

## Why Use This Utility

- Prevent your PC from going to sleep during long downloads, file transfers, or simulations
- Automatically shut down your PC after a set time to save power
- Monitor system resources while running long-term processes
- Customize the way your PC stays awake to match your needs

## Development Status

This utility is provided as-is for testing purposes. The console version can be run in any environment, while the GUI version requires a Windows environment with display and input capabilities.

## License

This project is for educational and testing purposes only.