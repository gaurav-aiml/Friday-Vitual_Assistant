from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from features import app_launcher, power_control, system_control


class LinuxSystemControlTests(unittest.TestCase):
    @patch("features.system_control.shutil.which", return_value="/usr/bin/wpctl")
    @patch("features.system_control.subprocess.run")
    def test_volume_up_uses_wpctl(self, run, _which):
        run.side_effect = [
            subprocess.CompletedProcess(
                args=[], returncode=0, stdout="Volume: 0.30\n", stderr=""
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("volume up")

        self.assertEqual(response, "Volume at 40%")
        self.assertEqual(
            run.call_args_list[0].args[0],
            ["/usr/bin/wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"],
        )
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["/usr/bin/wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "0.40"],
        )

    @patch("features.system_control.shutil.which", return_value=None)
    def test_missing_volume_utility_is_reported(self, _which):
        response = system_control.handle_command("volume up")

        self.assertIn("Linux volume controls require wpctl or pactl", response)

    @patch(
        "features.system_control.shutil.which",
        side_effect=lambda name: "/usr/bin/pactl" if name == "pactl" else None,
    )
    @patch("features.system_control.subprocess.run")
    def test_volume_setting_falls_back_to_pactl(self, run, _which):
        run.side_effect = [
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout="Volume: front-left: 9830 / 30% / -30.00 dB\n",
                stderr="",
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("volume 75")

        self.assertEqual(response, "Volume set to 75%")
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["/usr/bin/pactl", "set-sink-volume", "@DEFAULT_SINK@", "75%"],
        )

    @patch(
        "features.system_control.shutil.which",
        side_effect=lambda name: "/usr/bin/brightnessctl" if name == "brightnessctl" else None,
    )
    @patch("features.system_control.subprocess.run")
    def test_brightness_up_uses_brightnessctl(self, run, _which):
        run.side_effect = [
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout="intel_backlight,backlight,500,937,53%\n",
                stderr="",
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("brightness up")

        self.assertEqual(response, "Brightness at 63%")
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["/usr/bin/brightnessctl", "set", "63%"],
        )


class LinuxDesktopCommandTests(unittest.TestCase):
    @patch("features.power_control.subprocess.run")
    def test_shutdown_schedules_one_minute_and_reports_that_delay(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

        response = power_control.handle_command("shutdown pc")

        self.assertEqual(
            response, "Shutting down in 1 minute. Say 'shutdown abort' to cancel."
        )
        self.assertEqual(
            run.call_args.args[0], ["shutdown", "--poweroff", "+1"]
        )

    @patch("features.power_control.subprocess.run")
    def test_cancel_shutdown_uses_linux_shutdown_command(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

        response = power_control.handle_command("cancel shutdown")

        self.assertEqual(response, "Shutdown cancelled.")
        self.assertEqual(run.call_args.args[0], ["shutdown", "-c"])

    @patch("features.power_control.subprocess.run")
    def test_lock_and_sleep_use_linux_session_commands(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

        self.assertEqual(
            power_control.handle_command("lock pc"), "Locking your screen."
        )
        self.assertEqual(run.call_args.args[0], ["loginctl", "lock-session"])

        self.assertEqual(
            power_control.handle_command("sleep pc"), "Going to sleep."
        )
        self.assertEqual(run.call_args.args[0], ["systemctl", "suspend"])

    @patch("features.app_launcher.shutil.which")
    @patch("features.app_launcher.subprocess.Popen")
    def test_terminal_launcher_uses_first_installed_linux_candidate(
        self, popen, which
    ):
        which.side_effect = lambda name: (
            "/usr/bin/gnome-terminal" if name == "gnome-terminal" else None
        )

        response = app_launcher.handle_command("open terminal")

        self.assertEqual(response, "Opening terminal.")
        popen.assert_called_once_with(["/usr/bin/gnome-terminal"])


if __name__ == "__main__":
    unittest.main()
