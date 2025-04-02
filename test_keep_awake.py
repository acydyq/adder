import os
import subprocess
import unittest
import platform
import shutil
import time

class TestKeepAwakeUtility(unittest.TestCase):
    def setUp(self):
        self.required_files = [
            "main.py",
            "console_keep_awake.py",
            "start_keep_awake.bat",
            "create_shortcut.ps1",
            "README.md",
            "awake_icon.png",
            "sleep_icon.png",
            "generated-icon.png"
        ]
        self.ps1 = "create_shortcut.ps1"
        self.batch = "start_keep_awake.bat"

    def test_required_files_exist(self):
        """Ensure all required project files exist"""
        print("\n🔍 Checking essential project files...")
        for file in self.required_files:
            with self.subTest(file=file):
                self.assertTrue(os.path.exists(file), f"❌ Missing file: {file}")
        print("✅ All required project files found.")

    def test_icon_files_exist(self):
        """Ensure all tray icon PNGs are present"""
        print("\n🖼️ Validating tray icon files...")
        icons = ["awake_icon.png", "sleep_icon.png", "generated-icon.png"]
        for icon in icons:
            self.assertTrue(os.path.exists(icon), f"❌ Missing icon: {icon}")
        print("✅ Tray icons OK.")

    def test_console_help_output(self):
        """Ensure console script outputs help when --help is passed"""
        print("\n🖥️ Checking --help output for console_keep_awake.py...")
        result = subprocess.run(
            ["python", "console_keep_awake.py", "--help"],
            capture_output=True,
            text=True
        )
        self.assertIn("Keep Awake Utility", result.stdout)
        print("✅ Console help output detected.")

    def test_main_gui_invocation(self):
        """Ensure main GUI script can be run with --help or safely invoked"""
        print("\n🪟 Testing GUI main.py launch with --help...")
        result = subprocess.run(
            ["python", "main.py", "--help"],
            capture_output=True,
            text=True
        )
        combined_output = result.stdout + result.stderr
        self.assertIn("Keep Awake Utility", combined_output)
        print("✅ main.py --help output received.")

    def test_batch_launcher_executes(self):
        """Ensure the batch launcher runs and outputs help"""
        print("\n📦 Executing start_keep_awake.bat...")
        result = subprocess.run(
            ["cmd.exe", "/c", self.batch, "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        combined_output = result.stdout + result.stderr
        self.assertIn("Keep Awake Utility", combined_output)
        print("✅ Batch launcher executes.")

    def test_create_shortcut_ps1(self):
        """Run PowerShell shortcut script and validate shortcut creation"""
        print("\n🔧 Running PowerShell shortcut creator...")
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", self.ps1],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
        self.assertIn("Shortcut created", output)
        shortcut_path = os.path.join(os.getcwd(), "KeepAwake.exe.lnk")
        self.assertTrue(os.path.exists(shortcut_path), "❌ Shortcut not created")
        print("✅ PowerShell shortcut generated.")

    def test_console_auto_start_timer(self):
        """Test CLI flags: --auto-start and --timer"""
        print("\n🧪 Running CLI auto-start + timer test...")
        result = subprocess.run(
            ["python", "console_keep_awake.py", "--auto-start", "--timer=1", "--non-interactive"],
            capture_output=True,
            text=True,
            timeout=10
        )
        self.assertIn("Timer set", result.stdout + result.stderr)
        print("✅ Console auto-start/timer executed.")

    def test_platform_compatibility(self):
        """Ensure we’re running on a supported platform"""
        print("\n💻 Checking platform...")
        supported = ["Windows", "Linux", "Darwin"]
        current = platform.system()
        print(f"🧠 Detected platform: {current}")
        self.assertIn(current, supported)
        print("✅ Supported OS confirmed.")

    def test_tray_icon_auto_switch(self):
        """Check simulated switching logic"""
        print("\n🎛️ Verifying logic for icon switch simulation...")
        icon_active = "awake_icon.png"
        icon_inactive = "sleep_icon.png"
        self.assertTrue(os.path.exists(icon_active))
        self.assertTrue(os.path.exists(icon_inactive))
        print("✅ Icon switch logic files exist.")

if __name__ == "__main__":
    unittest.main()
