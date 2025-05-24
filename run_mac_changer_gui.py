import sys
import os

def main():
    # Support both .venv and venv
    gui_path = os.path.join(os.path.dirname(__file__), "src", "mac_changer_gui.py")
    if not os.path.exists(gui_path):
        print(f"ERROR: {gui_path} does not exist.")
        sys.exit(1)
    print(f"Running: {sys.executable} {gui_path}")
    os.execv(sys.executable, [sys.executable, gui_path])

if __name__ == "__main__":
    main()
