# Keep Awake Utility

A Python-based utility to prevent your PC from sleeping or locking by simulating activity. Offers both a GUI interface with system tray support and a cross-platform command-line version.

---

## Features

- Simulates mouse and keyboard activity to prevent sleep
- Auto-shutdown timer (1, 2, 5, or 10 hours)
- System tray integration (GUI mode)
- Tray icon switches dynamically (awake/sleep)
- Real-time tooltip shows timer countdown and status
- Command-line interface with automation support
- Launcher batch file and shortcut generator script
- Cross-platform console version (Windows/Linux/macOS)
- Auto-start CLI and max timer modes
- Full test suite to validate behavior

---

## Requirements

- Python 3.6+
- `pyautogui`, `psutil`, `pillow`, `pystray`
- Windows recommended for full GUI support

Install dependencies:
```bash
pip install pyautogui psutil pillow pystray
```

---

## Usage

### GUI Version
```bash
python main.py --auto-start --timer=2
```

### Console Version
```bash
python console_keep_awake.py --auto-start --timer=5 --non-interactive
```

### Help Flags
- `--help` or `-h`: Show usage info
- `--auto-start`: Begin simulating activity immediately
- `--timer=N`: Shutdown in N hours
- `--max-timer`: Use 10-hour timer
- `--non-interactive`: Skip CLI prompt

---

## System Tray Behavior (GUI)

The GUI runs silently in the background:

- `awake_icon.png`: tray icon when active
- `sleep_icon.png`: tray icon when inactive
- `generated-icon.png`: fallback if others are missing
- Tooltip displays current status and remaining time
- Icons update every 5 seconds

---

## Batch Launcher

Run:
```bat
start_keep_awake.bat
```

Choose from:
1. GUI Version
2. Console Version
3. Background Mode
4. Exit

---

## Shortcut Creation (Windows)

Create a `.lnk` with tray icon:
```powershell
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1
```

Creates:
- `KeepAwake.exe.lnk`
- Uses `awake_icon.png` or `generated-icon.png`

---

## Testing

Run:
```bash
python test_keep_awake.py
```

Verifies:
- Icons and scripts exist
- Console and GUI launch correctly
- CLI flags function properly
- PowerShell and batch files execute

---

## Files Overview

| File | Description |
|------|-------------|
| `main.py` | GUI mode with system tray |
| `console_keep_awake.py` | Terminal-based control |
| `start_keep_awake.bat` | Launcher menu script |
| `create_shortcut.ps1` | Windows shortcut creator |
| `README.md` | Full documentation |
| `test_keep_awake.py` | Test suite |
| `awake_icon.png` | Active tray icon |
| `sleep_icon.png` | Inactive tray icon |
| `generated-icon.png` | Default/fallback icon |

---

## License

MIT License – Use freely for personal or professional purposes. No warranties or guarantees.

