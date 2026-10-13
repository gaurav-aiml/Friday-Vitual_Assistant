from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from features import app_launcher, power_control, system_control


class WindowsSystemControlTests(unittest.TestCase):
    @patch("features.system_control.subprocess.run")
    def test_volume_up_uses_windows_audio_api(self, run):
        run.side_effect = [
            subprocess.CompletedProcess(
                args=[], returncode=0, stdout="30\n", stderr=""
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("volume up")

        self.assertEqual(response, "Volume at 40%")
        self.assertEqual(
            run.call_args_list[0].args[0][:3],
            ["powershell", "-NoProfile", "-Command"],
        )
        self.assertIn("CurrentVolume", run.call_args_list[0].args[0][3])
        self.assertIn("SetVolume(40)", run.call_args_list[1].args[0][3])

    @patch(
        "features.system_control.subprocess.run",
        side_effect=FileNotFoundError("powershell"),
    )
    def test_missing_powershell_is_reported(self, _run):
        response = system_control.handle_command("volume up")

        self.assertIn("Windows 11 audio controls require PowerShell", response)

    @patch("features.system_control.subprocess.run")
    def test_brightness_up_uses_wmi_globally(self, run):
        run.side_effect = [
            subprocess.CompletedProcess(
                args=[], returncode=0, stdout="50\n", stderr=""
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("brightness up")

        self.assertEqual(response, "Brightness at 60%")
        self.assertIn("WmiSetBrightness", run.call_args_list[1].args[0][3])


class WindowsDesktopCommandTests(unittest.TestCase):
    @patch("features.power_control.subprocess.run")
    def test_shutdown_schedules_one_minute_and_reports_that_delay(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

        response = power_control.handle_command("shutdown pc")

        self.assertEqual(
            response, "Shutting down in 1 minute. Say 'shutdown abort' to cancel."
        )
        self.assertEqual(run.call_args.args[0], ["shutdown", "/s", "/t", "60"])

    @patch("features.app_launcher.shutil.which")
    @patch("features.app_launcher.subprocess.Popen")
    def test_terminal_launcher_uses_first_installed_windows_candidate(
        self, popen, which
    ):
        which.side_effect = lambda name: (
            "C:/Windows/System32/cmd.exe" if name == "cmd.exe" else None
        )

        response = app_launcher.handle_command("open terminal")

        self.assertEqual(response, "Opening terminal.")
        popen.assert_called_once_with(["C:/Windows/System32/cmd.exe"])


if __name__ == "__main__":
    unittest.main()
