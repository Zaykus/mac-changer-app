# MAC Changer Application

A Windows application that allows users to view and change MAC addresses through a modern, user-friendly GUI.

## Features

### Current Features
- Dark theme modern interface
- List all network adapters
- View current MAC address
- Generate random MAC addresses
- Enable/disable manual MAC address ("Value"/"Not Present")
- Change MAC address manually
- Restart network adapters
- PowerShell-based adapter control (Windows 10/11)
- Administrator rights handling

### Planned Features
- Show adapter details (status, IP, etc.)
- Theme toggle (dark/light)
- Help/About dialog
- MAC address history
- Adapter filtering
- Standalone executable
- More accessibility options

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mac-changer-app
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
1. Double-click `run_mac_changer_gui.bat`
2. Allow administrator access when prompted
3. Select your network adapter
4. Choose to:
   - Enable/disable manual MAC ("Value"/"Not Present")
   - Generate a random MAC
   - Enter a custom MAC
   - Change or restore the MAC address
   - Restart the network adapter

### Manual Start
```
cd path\to\mac-changer-app
python run_mac_changer_gui.py
```

## Requirements
- Windows 10/11
- Python 3.7+
- Administrator privileges
- PyQt5 (included in requirements.txt)

## Troubleshooting

### Common Issues
- **Administrator Access Required**: Run with admin rights
- **Network Adapter Not Showing**: Refresh the adapter list
- **MAC Not Changing**: 
  1. Ensure adapter supports MAC changes
  2. Enable manual MAC address
  3. Click "Restart Network" after changes

### Error Messages
- "Failed to change MAC": Check administrator rights
- "No adapter selected": Choose an adapter first
- "Invalid MAC address": Use format XX:XX:XX:XX:XX:XX

## Contributing

Issues and pull requests are welcome. Please follow the existing code style.

## License

MIT License - See LICENSE file for details