from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from features import app_launcher, power_control, system_control


class LinuxSystemControlTests(unittest.TestCase):
    @patch("features.system_control.subprocess.run")
    def test_volume_up_uses_pactl(self, run):
        run.side_effect = [
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout="Volume: front-left: 19661 / 30% / -31.37 dB",
                stderr="",
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("volume up")

        self.assertEqual(response, "Volume at 40%")
        self.assertEqual(
            run.call_args_list[0].args[0],
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
        )
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "40%"],
        )

    @patch(
        "features.system_control.subprocess.run",
        side_effect=FileNotFoundError("pactl"),
    )
    def test_missing_pactl_is_reported(self, _run):
        response = system_control.handle_command("volume up")

        self.assertIn("install pulseaudio-utils", response)

    @patch("features.system_control.subprocess.run")
    def test_brightness_up_uses_brightnessctl(self, run):
        run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout="50\n", stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="100\n", stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]

        response = system_control.handle_command("brightness up")

        self.assertEqual(response, "Brightness at 60%")
        self.assertEqual(run.call_args_list[2].args[0], ["brightnessctl", "set", "60%"])


class LinuxDesktopCommandTests(unittest.TestCase):
    @patch("features.power_control.subprocess.run")
    def test_shutdown_schedules_one_minute_and_reports_that_delay(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

        response = power_control.handle_command("shutdown pc")

        self.assertEqual(response, "Shutting down in 1 minute. Say 'shutdown abort' to cancel.")
        self.assertEqual(run.call_args.args[0], ["shutdown", "-h", "+1"])

    @patch("features.app_launcher.shutil.which")
    @patch("features.app_launcher.subprocess.Popen")
    def test_terminal_launcher_uses_first_installed_candidate(self, popen, which):
        which.side_effect = lambda name: "/usr/bin/kgx" if name == "kgx" else None

        response = app_launcher.handle_command("open terminal")

        self.assertEqual(response, "Opening terminal.")
        popen.assert_called_once_with(["/usr/bin/kgx"])


if __name__ == "__main__":
    unittest.main()
