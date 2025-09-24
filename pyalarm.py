#!/usr/bin/env python3
"""
PyAlarm - A cross-platform system tray time alarm application.

This application sits in your system tray and plays configurable sounds at
specific times during work hours to help with time management and awareness.

Author: PyAlarm Contributors
License: MIT
"""

import sys
import os
import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import pygame
import pystray
from PIL import Image
from pystray import MenuItem as item


class Config:
    """Handles configuration management with persistent JSON storage."""
    def __init__(self) -> None:
        """Initialize configuration with default values."""
        self.config_file: Path = Path(__file__).parent / "config.json"
        self.default_config: Dict[str, Any] = {
            "work_start_hour": 8,
            "work_end_hour": 18,
            "sound_enabled": True
        }
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from JSON file, create with defaults if not found."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    # Ensure all default keys exist
                    for key, value in self.default_config.items():
                        if key not in self.config:
                            self.config[key] = value
            else:
                self.config = self.default_config.copy()
                self.save_config()
        except Exception:
            self.config = self.default_config.copy()

    def save_config(self) -> None:
        """Save current configuration to JSON file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def get(self, key: str) -> Any:
        """Get configuration value with fallback to default."""
        return self.config.get(key, self.default_config.get(key))

    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save to file."""
        self.config[key] = value
        self.save_config()

class AlarmTimer(threading.Thread):
    """Background thread that monitors time and triggers alarms."""

    def __init__(self, config: Config, app: 'PyAlarmApp') -> None:
        """Initialize alarm timer thread.

        Args:
            config: Configuration instance
            app: Main application instance for playing alarms
        """
        super().__init__()
        self.config = config
        self.app = app
        self.running = True
        self.daemon = True

    def run(self) -> None:
        """Main loop that checks time and triggers alarms."""
        last_trigger = {"halfpast": -1, "bell": -1}

        while self.running:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            work_start = self.config.get("work_start_hour")
            work_end = self.config.get("work_end_hour")

            # Only trigger alarms during work hours
            if work_start <= current_hour < work_end:
                # Check for HalfPast at 29 minutes past
                if current_minute == 29 and last_trigger["halfpast"] != current_hour:
                    self.app.play_alarm("halfpast")
                    last_trigger["halfpast"] = current_hour
                # Check for Bell at 59 minutes past
                elif current_minute == 59 and last_trigger["bell"] != current_hour:
                    self.app.play_alarm("bell")
                    last_trigger["bell"] = current_hour

            time.sleep(30)  # Check every 30 seconds

    def stop(self) -> None:
        """Stop the alarm timer thread."""
        self.running = False

class PyAlarmApp:
    """Main application class that manages the system tray and alarms."""

    def __init__(self) -> None:
        """Initialize the PyAlarm application."""
        self.config = Config()

        # Initialize pygame for sound
        pygame.mixer.init()

        # Paths to resources
        self.base_path = Path(__file__).parent
        self.active_icon = str(self.base_path / "Active.png")
        self.inactive_icon = str(self.base_path / "Inactive.png")
        self.paused_icon = str(self.base_path / "Paused.png")
        self.bell_sound = str(self.base_path / "Bell.wav")
        self.halfpast_sound = str(self.base_path / "HalfPast.wav")

        # State management
        self.is_paused = False
        self.pause_until: Optional[datetime] = None

        # Load images
        self.active_image = Image.open(self.active_icon) if os.path.exists(self.active_icon) else None
        self.inactive_image = Image.open(self.inactive_icon) if os.path.exists(self.inactive_icon) else None
        self.paused_image = Image.open(self.paused_icon) if os.path.exists(self.paused_icon) else None

        # Create system tray icon
        self.setup_tray_icon()

        # Start update timer in a separate thread
        self.update_timer_thread = threading.Thread(target=self.update_timer_loop, daemon=True)
        self.update_timer_thread.start()

        # Alarm timer thread
        self.alarm_timer = AlarmTimer(self.config, self)
        self.alarm_timer.start()

    def setup_tray_icon(self) -> None:
        """Set up the system tray icon and context menu."""
        # Create menu
        menu = pystray.Menu(
            item("🔊 Test HalfPast Sound (:29)", lambda: self.test_sound("halfpast")),
            item("🔔 Test Bell Sound (:59)", lambda: self.test_sound("bell")),
            pystray.Menu.SEPARATOR,
            item("Pause for 30 minutes", lambda: self.pause_alarms(30)),
            item("Pause for 60 minutes", lambda: self.pause_alarms(60)),
            pystray.Menu.SEPARATOR,
            item("Resume", self.unpause_alarms, enabled=lambda item: self.is_paused),
            pystray.Menu.SEPARATOR,
            item("Work Hours", pystray.Menu(
                item("6:00 - 16:00", lambda: self.set_work_hours(6, 16),
                     checked=lambda item: self.config.get("work_start_hour") == 6 and self.config.get("work_end_hour") == 16),
                item("7:00 - 17:00", lambda: self.set_work_hours(7, 17),
                     checked=lambda item: self.config.get("work_start_hour") == 7 and self.config.get("work_end_hour") == 17),
                item("8:00 - 18:00", lambda: self.set_work_hours(8, 18),
                     checked=lambda item: self.config.get("work_start_hour") == 8 and self.config.get("work_end_hour") == 18),
                item("9:00 - 19:00", lambda: self.set_work_hours(9, 19),
                     checked=lambda item: self.config.get("work_start_hour") == 9 and self.config.get("work_end_hour") == 19),
            )),
            pystray.Menu.SEPARATOR,
            item("Exit", self.exit_app)
        )

        # Create tray icon
        self.icon = pystray.Icon(
            "PyAlarm",
            self.get_current_image(),
            menu=menu
        )

    def get_current_image(self) -> Optional[Image.Image]:
        """Get the appropriate tray icon based on current state."""
        now = datetime.now()

        # Check if pause has expired
        if self.is_paused and self.pause_until and now >= self.pause_until:
            self.is_paused = False
            self.pause_until = None

        # Determine which icon to show
        if self.is_paused:
            return self.paused_image or self.active_image
        else:
            work_start = self.config.get("work_start_hour")
            work_end = self.config.get("work_end_hour")
            current_hour = now.hour

            if work_start <= current_hour < work_end:
                return self.active_image
            else:
                return self.inactive_image or self.active_image

    def update_timer_loop(self) -> None:
        """Background loop to update tray icon state periodically."""
        while True:
            time.sleep(60)  # Update every minute
            if hasattr(self, 'icon'):
                self.icon.icon = self.get_current_image()

    def set_work_hours(self, start_hour: int, end_hour: int) -> None:
        """Set work hours configuration."""
        self.config.set("work_start_hour", start_hour)
        self.config.set("work_end_hour", end_hour)

    def pause_alarms(self, minutes: int) -> None:
        """Pause alarms for specified number of minutes."""
        self.is_paused = True
        self.pause_until = datetime.now() + timedelta(minutes=minutes)
        if hasattr(self, 'icon'):
            self.icon.icon = self.get_current_image()

    def unpause_alarms(self) -> None:
        """Resume alarms from paused state."""
        self.is_paused = False
        self.pause_until = None
        if hasattr(self, 'icon'):
            self.icon.icon = self.get_current_image()

    def test_sound(self, alarm_type: str) -> None:
        """Play a test sound manually from the menu."""
        try:
            if alarm_type == "halfpast" and os.path.exists(self.halfpast_sound):
                pygame.mixer.music.load(self.halfpast_sound)
                pygame.mixer.music.play()
            elif alarm_type == "bell" and os.path.exists(self.bell_sound):
                pygame.mixer.music.load(self.bell_sound)
                pygame.mixer.music.play()
        except Exception:
            pass

    def play_alarm(self, alarm_type: str) -> None:
        """Play alarm sound if conditions are met."""
        # Don't play alarms if paused
        if self.is_paused:
            return

        # Don't play alarms outside work hours (double check)
        now = datetime.now()
        work_start = self.config.get("work_start_hour")
        work_end = self.config.get("work_end_hour")
        if not (work_start <= now.hour < work_end):
            return

        try:
            if alarm_type == "halfpast" and os.path.exists(self.halfpast_sound):
                pygame.mixer.music.load(self.halfpast_sound)
                pygame.mixer.music.play()
            elif alarm_type == "bell" and os.path.exists(self.bell_sound):
                pygame.mixer.music.load(self.bell_sound)
                pygame.mixer.music.play()
        except Exception:
            pass

    def exit_app(self) -> None:
        """Clean up and exit the application."""
        self.alarm_timer.stop()
        if hasattr(self, 'icon'):
            self.icon.stop()

    def run(self) -> None:
        """Start the system tray application."""
        self.icon.run()

def main() -> None:
    """Entry point for the application."""
    app = PyAlarmApp()
    app.run()

if __name__ == "__main__":
    main()