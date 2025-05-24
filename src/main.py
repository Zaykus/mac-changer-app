# main.py

import sys
from ui import UserInterface
from mac_changer import MacChanger

def main():
    mac_changer = MacChanger()
    ui = UserInterface(mac_changer)

    try:
        ui.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()