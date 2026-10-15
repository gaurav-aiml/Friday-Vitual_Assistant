from __future__ import annotations

import unittest
from unittest.mock import patch

from features import app_launcher, power_control, system_control


class WindowsSystemControlTests(unittest.TestCase):
    @patch("features.system_control.platform.system", return_value="Windows")
    @patch("features.system_control._set_windows_volume")
    @patch("features.system_control._get_windows_volume", return_value=30)
    def test_volume_up_uses_windows_audio_backend(self, _get_volume, set_volume, _os):
        response = system_control.handle_command("volume up")

        self.assertEqual(response, "Volume at 40%")
        set_volume.assert_called_once_with(40)

    @patch("features.system_control.platform.system", return_value="Windows")
    @patch("features.system_control._get_windows_brightness", return_value=50)
    @patch("features.system_control._set_windows_brightness")
    def test_brightness_up_uses_windows_display_backend(
        self, set_brightness, _get_brightness, _os
    ):
        response = system_control.handle_command("brightness up")

        self.assertEqual(response, "Brightness at 60%")
        set_brightness.assert_called_once_with(60)


class WindowsPowerCommandTests(unittest.TestCase):
    @patch("features.power_control.platform.system", return_value="Windows")
    @patch("features.power_control.subprocess.run")
    def test_shutdown_uses_windows_command(self, run, _os):
        self.assertIn("1 minute", power_control.handle_command("shutdown pc"))
        self.assertEqual(run.call_args.args[0], ["shutdown", "/s", "/t", "60"])

    @patch("features.power_control.platform.system", return_value="Windows")
    @patch("features.power_control.subprocess.run")
    def test_cancel_shutdown_uses_windows_command(self, run, _os):
        self.assertEqual(power_control.handle_command("cancel shutdown"), "Shutdown cancelled.")
        self.assertEqual(run.call_args.args[0], ["shutdown", "/a"])

    @patch("features.power_control.platform.system", return_value="Windows")
    @patch("features.power_control.subprocess.run")
    def test_lock_and_sleep_use_windows_commands(self, run, _os):
        self.assertEqual(power_control.handle_command("lock pc"), "Locking your screen.")
        self.assertEqual(
            run.call_args.args[0], ["rundll32.exe", "user32.dll,LockWorkStation"]
        )

        self.assertEqual(power_control.handle_command("sleep pc"), "Going to sleep.")
        self.assertEqual(
            run.call_args.args[0],
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
        )


class WindowsAppLauncherTests(unittest.TestCase):
    @patch("features.app_launcher.platform.system", return_value="Windows")
    @patch("features.app_launcher.shutil.which", return_value=r"C:\Windows\notepad.exe")
    @patch("features.app_launcher.subprocess.Popen")
    def test_notepad_launch_uses_windows_executable(self, popen, _which, _os):
        response = app_launcher.handle_command("open notepad")

        self.assertEqual(response, "Opening notepad.")
        popen.assert_called_once_with([r"C:\Windows\notepad.exe"])

    @patch("features.app_launcher.platform.system", return_value="Windows")
    @patch("features.app_launcher.shutil.which", return_value=r"C:\Tools\code.cmd")
    @patch("features.app_launcher.subprocess.Popen")
    def test_batch_launcher_uses_command_interpreter(self, popen, _which, _os):
        response = app_launcher.handle_command("open vscode")

        self.assertEqual(response, "Opening vscode.")
        self.assertEqual(
            popen.call_args.args[0],
            ["cmd.exe", "/c", r"C:\Tools\code.cmd"],
        )


if __name__ == "__main__":
    unittest.main()
