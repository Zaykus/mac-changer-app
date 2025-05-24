import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox, QHBoxLayout, QFrame, QCheckBox, QAction, QMenuBar, QMenu
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSettings, QPoint, QSize
from mac_changer import MacChanger
from utils.mac_history import MacHistory
from utils.logger import Logger
from typing import Dict, Optional

class MacChangerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.mac_history = MacHistory()
        self.logger = Logger()
        self.setWindowTitle("Windows MAC Changer")
        self.setWindowIcon(QIcon())
        self.setStyleSheet("background-color: #23272f; color: #f8f8f2;")
        self.mac_changer = MacChanger()
        self.adapters = self.mac_changer.get_adapters()

        self.adapter_label = QLabel("Select Network Adapter:")
        self.adapter_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.adapter_combo = QComboBox()
        for _, desc, _ in self.adapters:
            self.adapter_combo.addItem(desc)
        self.adapter_combo.currentIndexChanged.connect(self.update_current_mac)

        self.current_mac_label = QLabel("Current MAC Address:")
        self.current_mac_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.current_mac_value = QLabel("")
        self.current_mac_value.setFont(QFont("Consolas", 11))
        self.current_mac_value.setStyleSheet("color: #50fa7b;")

        # Checkbox for manual MAC address
        self.manual_mac_checkbox = QCheckBox("Enable manual MAC address (Value)")
        self.manual_mac_checkbox.setChecked(True)
        self.manual_mac_checkbox.setStyleSheet("font-weight: bold;")
        self.manual_mac_checkbox.stateChanged.connect(self.on_manual_mac_toggle)

        self.mac_label = QLabel("New MAC Address:")
        self.mac_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.mac_input = QLineEdit()
        self.mac_input.setFont(QFont("Consolas", 11))
        self.random_btn = QPushButton("Random")
        self.random_btn.setStyleSheet("background-color: #6272a4; color: #fff;")
        self.random_btn.clicked.connect(self.set_random_mac)

        self.change_btn = QPushButton("Change MAC")
        self.change_btn.setStyleSheet("background-color: #50fa7b; color: #23272f; font-weight: bold;")
        self.change_btn.clicked.connect(self.on_change)

        self.restore_btn = QPushButton("Restore Original MAC")
        self.restore_btn.setStyleSheet("background-color: #ffb86c; color: #23272f; font-weight: bold;")
        self.restore_btn.clicked.connect(self.on_restore)

        self.restart_btn = QPushButton("Restart Network")
        self.restart_btn.setStyleSheet("background-color: #8be9fd; color: #23272f; font-weight: bold;")
        self.restart_btn.clicked.connect(self.on_restart)

        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setStyleSheet("background-color: #ff5555; color: #fff; font-weight: bold;")
        self.exit_btn.clicked.connect(self.close)

        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #f1fa8c; padding: 8px;")

        # Menu bar with Help/About
        self.menu_bar = QMenuBar(self)
        help_menu = QMenu("Help", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        self.menu_bar.addMenu(help_menu)

        # Layouts
        mac_input_layout = QHBoxLayout()
        mac_input_layout.addWidget(self.mac_input)
        mac_input_layout.addWidget(self.random_btn)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.change_btn)
        btn_layout.addWidget(self.restore_btn)
        btn_layout.addWidget(self.restart_btn)
        btn_layout.addWidget(self.exit_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.adapter_label)
        layout.addWidget(self.adapter_combo)
        layout.addWidget(self.current_mac_label)
        layout.addWidget(self.current_mac_value)
        layout.addWidget(self.manual_mac_checkbox)
        layout.addWidget(self.mac_label)
        layout.addLayout(mac_input_layout)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # Add theme support
        self.settings = QSettings('MAC Changer', 'GUI')
        self.dark_theme = True
        self.load_settings()

        # Add details button
        self.details_btn = QPushButton("Show Details")
        self.details_btn.clicked.connect(self.show_adapter_details)

        # Add theme toggle
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)

        btn_layout.addWidget(self.details_btn)
        btn_layout.addWidget(self.theme_btn)

        self.update_current_mac()
        self.on_manual_mac_toggle()  # Set initial state

    def load_settings(self) -> None:
        """Load window settings and theme preference."""
        pos = self.settings.value('pos', QPoint(200, 200))
        size = self.settings.value('size', QSize(540, 340))
        self.dark_theme = self.settings.value('dark_theme', True, type=bool)

        self.move(pos)
        self.resize(size)
        self.apply_theme()

    def closeEvent(self, event) -> None:
        """Save window settings before closing."""
        self.settings.setValue('pos', self.pos())
        self.settings.setValue('size', self.size())
        self.settings.setValue('dark_theme', self.dark_theme)
        event.accept()

    def apply_theme(self) -> None:
        """Apply the current theme."""
        if self.dark_theme:
            self.setStyleSheet("""
                QWidget { background-color: #23272f; color: #f8f8f2; }
                QPushButton { 
                    background-color: #6272a4; 
                    color: #fff;
                    padding: 5px;
                    border: none;
                    border-radius: 3px;
                }
                QComboBox { 
                    background-color: #3d4451;
                    border: 1px solid #6272a4;
                    padding: 5px;
                }
                QLineEdit {
                    background-color: #3d4451;
                    border: 1px solid #6272a4;
                    padding: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f0f0f0; color: #2c3e50; }
                QPushButton { 
                    background-color: #3498db; 
                    color: white;
                    padding: 5px;
                    border: none;
                    border-radius: 3px;
                }
                QComboBox { 
                    background-color: white;
                    border: 1px solid #bdc3c7;
                    padding: 5px;
                }
                QLineEdit {
                    background-color: white;
                    border: 1px solid #bdc3c7;
                    padding: 5px;
                }
            """)

    def update_current_mac(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.current_mac_value.setText("")
            return
        net_cfg_id, _, reg_path = self.adapters[idx]
        mac = self.mac_changer.get_current_mac(net_cfg_id)
        self.current_mac_value.setText(mac or "Unknown")
        # Check if manual MAC is enabled (NetworkAddress present)
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                val, _ = winreg.QueryValueEx(key, "NetworkAddress")
                if val:
                    self.manual_mac_checkbox.setChecked(True)
                else:
                    self.manual_mac_checkbox.setChecked(False)
        except FileNotFoundError:
            self.manual_mac_checkbox.setChecked(False)
        except Exception:
            self.manual_mac_checkbox.setChecked(False)
        self.status_label.setText("")

    def set_random_mac(self):
        self.mac_input.setText(self.mac_changer.generate_random_mac())
        self.status_label.setText("Generated a random MAC address.")

    def on_change(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.show_error("No adapter selected.")
            return
            
        net_cfg_id, _, reg_path = self.adapters[idx]
        current_mac = self.mac_changer.get_current_mac(net_cfg_id)
        new_mac = self.mac_input.text().strip()

        try:
            # Change MAC
            self.mac_changer.set_manual_mac_enabled(reg_path, True, new_mac)
            self.mac_changer.disable_enable_adapter(net_cfg_id)
            
            # Log the change
            self.logger.info(f"Changed MAC for {net_cfg_id} from {current_mac} to {new_mac}")
            
            # Add to history
            self.mac_history.add_entry(net_cfg_id, current_mac, new_mac)
            
            self.show_success("MAC address changed! Click 'Restart Network' if needed.")
            self.update_current_mac()
            
        except Exception as e:
            error_msg = f"Failed to change MAC address: {e}"
            self.logger.error(error_msg)
            self.show_error(error_msg)

    def on_restore(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.status_label.setText("No adapter selected.")
            return
        net_cfg_id, _, reg_path = self.adapters[idx]
        try:
            self.mac_changer.set_manual_mac_enabled(reg_path, False)
            self.mac_changer.disable_enable_adapter(net_cfg_id)
            self.status_label.setText("Manual MAC disabled (Not Present). Click 'Restart Network' if needed.")
            self.update_current_mac()
        except Exception as e:
            self.status_label.setText(f"Failed to disable manual MAC: {e}")

    def on_restart(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.status_label.setText("No adapter selected.")
            return
        net_cfg_id, _, _ = self.adapters[idx]
        try:
            self.mac_changer.restart_adapter(net_cfg_id)
            self.status_label.setText("Network adapter restarted!")
            self.update_current_mac()
        except Exception as e:
            self.status_label.setText(f"Failed to restart adapter: {e}")

    def on_manual_mac_toggle(self):
        checked = self.manual_mac_checkbox.isChecked()
        self.mac_input.setEnabled(checked)
        self.random_btn.setEnabled(checked)
        self.change_btn.setEnabled(checked)
        if not checked:
            # Set "Not Present" (remove NetworkAddress)
            idx = self.adapter_combo.currentIndex()
            if idx >= 0:
                net_cfg_id, _, reg_path = self.adapters[idx]
                try:
                    self.mac_changer.set_manual_mac_enabled(reg_path, False)
                    self.mac_changer.disable_enable_adapter(net_cfg_id)
                    self.status_label.setText("Manual MAC disabled (Not Present).")
                    self.update_current_mac()
                except Exception as e:
                    self.status_label.setText(f"Failed to disable manual MAC: {e}")

    # Not Implemented Yet: Show adapter details (status, IP, etc.)
    def show_adapter_details(self) -> None:
        """Show detailed information about the selected adapter."""
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.show_error("No adapter selected.")
            return

        net_cfg_id, _, _ = self.adapters[idx]
        details = self.mac_changer.get_adapter_details(net_cfg_id)
        
        # Add MAC history
        history = self.mac_history.get_history(net_cfg_id)
        if history:
            details["MAC History"] = f"Last {len(history)} changes"

        details_text = "\n".join(f"{k}: {v}" for k, v in details.items())
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Adapter Details")
        msg.setText(details_text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    # Not Implemented Yet: Better error popups (QMessageBox for errors/success)
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)

    # Not Implemented Yet: Theme toggle (dark/light)
    def toggle_theme(self) -> None:
        """Toggle between light and dark theme."""
        self.dark_theme = not self.dark_theme
        self.apply_theme()
        self.settings.setValue('dark_theme', self.dark_theme)
        self.logger.info(f"Theme changed to {'dark' if self.dark_theme else 'light'}")

    # Not Implemented Yet: Help/About dialog
    def show_about_dialog(self):
        QMessageBox.information(self, "About", "MAC Changer App\nNot Implemented Yet: About details.")

    # Not Implemented Yet: Window size/position persistence
    def load_window_settings(self):
        # Placeholder for loading window geometry
        pass

    def save_window_settings(self):
        # Placeholder for saving window geometry
        pass

    # Not Implemented Yet: Localization (multi-language)
    def set_language(self, lang_code):
        # Placeholder for language switching
        pass

    # Not Implemented Yet: Save/restore original MAC (true hardware MAC, not just registry)
    def save_original_mac(self):
        # Placeholder for saving hardware MAC
        pass

    def restore_original_mac(self):
        # Placeholder for restoring hardware MAC
        pass

    # Not Implemented Yet: MAC change history
    def add_mac_history(self, mac):
        # Placeholder for MAC history
        pass

    # Not Implemented Yet: Command line arguments for automation
    def handle_cli_args(self):
        # Placeholder for CLI automation
        pass

    # Not Implemented Yet: Adapter filtering (hide virtual/non-physical)
    def filter_adapters(self):
        # Placeholder for filtering adapters
        pass

    # Not Implemented Yet: Auto-detect admin rights in Python
    def check_admin_rights(self):
        # Placeholder for admin check
        pass

    # Not Implemented Yet: Refactor GUI/backend separation
    # (Would require major restructuring)

    # Not Implemented Yet: Type hints everywhere
    # (Add type hints to all methods)

    # Not Implemented Yet: Unit tests
    # (Add test suite in a separate test file)

    # Not Implemented Yet: Logging to file
    def log_event(self, event):
        # Placeholder for logging
        pass

    # Not Implemented Yet: Full docstrings
    # (Add docstrings to all methods)

    # Not Implemented Yet: PEP8 compliance
    # (Run linter/formatter)

    # Not Implemented Yet: Enhanced input validation
    def validate_mac(self, mac):
        # ...existing code...
        # Add more robust validation here
        pass

    # Not Implemented Yet: Admin check in Python
    def require_admin(self):
        # Placeholder for admin check
        pass

    # Not Implemented Yet: Standalone .exe (PyInstaller)
    # (Add PyInstaller spec file and instructions)

    # Not Implemented Yet: Installer
    # (Add installer script)

    # Not Implemented Yet: README with screenshots/FAQ
    # (Update README)

    # Not Implemented Yet: Uninstall/cleanup option
    def uninstall_cleanup(self):
        # Placeholder for cleanup logic
        pass

    # Not Implemented Yet: Adapter refresh button
    def refresh_adapters(self):
        # Placeholder for refreshing adapter list
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MacChangerApp()
    window.resize(540, 340)
    window.show()
    sys.exit(app.exec_())