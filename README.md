# 🔔 PyAlarm

A cross-platform system tray application that helps you stay aware of time during work hours by playing configurable sounds at specific intervals.

![PyAlarm Demo](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🖥️ System Tray Integration**: Unobtrusive icon that changes based on current state
- **⏰ Smart Time Alarms**:
  - HalfPast.wav at :29 minutes past each hour
  - Bell.wav at :59 minutes past each hour
- **🕐 Configurable Work Hours**: Set when alarms should be active (default: 8 AM - 6 PM)
- **⏸️ Flexible Pause System**: Right-click to pause for 30 or 60 minutes
- **🎵 Test Sounds**: Manual sound testing via context menu
- **💾 Persistent Settings**: Configuration automatically saved
- **🌍 Cross-Platform**: Windows, macOS, and Linux support

## 📸 Screenshots

The system tray icon changes to reflect the current state:
- 🟢 **Active.png**: During work hours, alarms enabled
- ⚫ **Inactive.png**: Outside work hours, alarms disabled
- 🟡 **Paused.png**: Alarms temporarily paused

## 🚀 Quick Start

### Option 1: Using pip (recommended)
```bash
pip install -r requirements.txt
python pyalarm.py
```

### Option 2: Using setup.py
```bash
python setup.py install
pyalarm
```

## 📋 Requirements

- **Python 3.7+**
- **Audio files**: `HalfPast.wav`, `Bell.wav`
- **Icon files**: `Active.png`, `Inactive.png`, `Paused.png`

### Dependencies
- `pygame` - Audio playback
- `pystray` - System tray integration
- `Pillow` - Image handling

## 🎛️ Usage

1. **Launch**: Run `python pyalarm.py`
2. **System Tray**: Look for the PyAlarm icon in your system tray
3. **Right-click** for options:
   - 🔊 Test HalfPast Sound (:29)
   - 🔔 Test Bell Sound (:59)
   - Pause for 30/60 minutes
   - Configure work hours
   - Exit

## ⚙️ Configuration

Settings are automatically saved to `config.json`:

```json
{
  "work_start_hour": 8,
  "work_end_hour": 18,
  "sound_enabled": true
}
```

### Work Hours Presets
- 6:00 - 16:00
- 7:00 - 17:00
- 8:00 - 18:00 (default)
- 9:00 - 19:00

## 📁 File Structure

```
pyalarm/
├── pyalarm.py          # Main application
├── requirements.txt    # Python dependencies
├── setup.py           # Installation script
├── Active.png         # Active state icon
├── Inactive.png       # Inactive state icon
├── Paused.png         # Paused state icon
├── Bell.wav           # Hour notification sound
├── HalfPast.wav       # Half-hour notification sound
├── config.json        # Auto-generated settings
├── LICENSE            # MIT License
└── README.md          # This file
```

## 🛠️ Development

### Running from Source
```bash
git clone https://github.com/yourusername/pyalarm.git
cd pyalarm
pip install -r requirements.txt
python pyalarm.py
```

### Code Quality
- Type hints throughout
- Comprehensive docstrings
- Clean error handling
- Thread-safe design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pystray](https://github.com/moses-palmer/pystray) for cross-platform system tray support
- Audio playback powered by [pygame](https://www.pygame.org/)
- Icons and sounds should be provided by the user

## ❓ FAQ

**Q: The app isn't playing sounds**
A: Check that your audio files exist and try the test sounds from the right-click menu.

**Q: How do I change the work hours?**
A: Right-click the tray icon → Work Hours → Select your preferred schedule.

**Q: Can I use custom sounds?**
A: Yes! Replace `Bell.wav` and `HalfPast.wav` with your own audio files.

**Q: The icon disappeared from my tray**
A: Restart the application. On some systems, you may need to enable system tray icons in your OS settings.

---

Made with ❤️ for better time awareness during work hours.