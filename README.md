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

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mac-changer-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the on-screen instructions to generate and change your MAC address.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.