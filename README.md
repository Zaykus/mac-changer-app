# MAC Changer Application

This project is a simple application that allows users to randomly change their MAC address through a graphical user interface (GUI). It is designed to be user-friendly and provides options for configuring the MAC address.

## Features

- Generate a random MAC address.
- Change the MAC address of a specified network interface.
- User-friendly graphical interface for easy interaction.

## Project Structure

```
mac-changer-app
├── src
│   ├── main.py          # Entry point of the application
│   ├── mac_changer.py   # Contains the MacChanger class for MAC address manipulation
│   ├── ui.py            # Defines the UserInterface class for GUI
│   └── config
│       └── __init__.py  # Configuration settings and constants
├── requirements.txt      # Lists dependencies for the project
└── README.md             # Documentation for the project
```

## Installation

### Option 1: Download the Latest Release (Recommended)

1.  Go to the [Releases page](https://github.com/YOUR_USERNAME/mac-changer-app/releases) of this repository.
2.  Download the latest release package (e.g., `mac-changer-app-v1.0.zip`).
3.  Extract the contents of the ZIP file to a directory of your choice.

### Option 2: Install from Source

1.  Clone the repository:
    ```
    git clone <repository-url>
    cd mac-changer-app
    ```

2.  Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

### Running the Application

#### From Latest Release (Recommended)

1.  Navigate to the extracted directory.
2.  Double-click `run_mac_changer_gui.bat` to launch the application with administrator privileges.

#### From Source

1.  Navigate to the project directory:
    ```
    cd path\to\mac-changer-app
    ```

2.  Run the application with administrator privileges:
    ```
    python run_mac_changer_gui.py
    ```

Follow the on-screen instructions to generate and change your MAC address.

## How to Run the App

### Requirements

- Windows 10/11
- Python 3.7+
- Administrator privileges (required for changing MAC addresses)
- Dependencies from `requirements.txt` (install with `pip install -r requirements.txt`)

## Troubleshooting

- **The app says `'wmic' is not recognized` or fails to change MAC:**  
  The app now uses PowerShell for adapter control. Make sure you are running as Administrator and on Windows 10/11.

- **Permission denied or registry errors:**  
  You must run the app as Administrator to change MAC addresses.

- **No adapters listed or MAC not changing:**  
  - Ensure your network adapter supports MAC address changes.
  - Some wireless adapters or virtual adapters may not support this feature.

- **Python or PyQt5 not found:**  
  - Install dependencies: `pip install -r requirements.txt`
  - Make sure Python is added to your system PATH.

- **App does not start or crashes:**  
  - Check that you are running the app from the correct folder.
  - Ensure all files are present and not blocked by antivirus.

- **Still having issues?**  
  - Open an issue on GitHub with your error message and system details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.