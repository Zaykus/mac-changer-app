import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt
from mac_changer import MacChanger

class MacChangerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows MAC Changer")
        self.setWindowIcon(QIcon())  # You can set a custom icon here if you have one
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

        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #f1fa8c; padding: 8px;")

        # Layouts
        mac_input_layout = QHBoxLayout()
        mac_input_layout.addWidget(self.mac_input)
        mac_input_layout.addWidget(self.random_btn)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.change_btn)
        btn_layout.addWidget(self.restore_btn)
        btn_layout.addWidget(self.restart_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.adapter_label)
        layout.addWidget(self.adapter_combo)
        layout.addWidget(self.current_mac_label)
        layout.addWidget(self.current_mac_value)
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

        self.update_current_mac()

    def update_current_mac(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.current_mac_value.setText("")
            return
        net_cfg_id, _, _ = self.adapters[idx]
        mac = self.mac_changer.get_current_mac(net_cfg_id)
        self.current_mac_value.setText(mac or "Unknown")
        self.status_label.setText("")

    def set_random_mac(self):
        self.mac_input.setText(self.mac_changer.generate_random_mac())
        self.status_label.setText("Generated a random MAC address.")

    def on_change(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.status_label.setText("No adapter selected.")
            return
        net_cfg_id, _, reg_path = self.adapters[idx]
        new_mac = self.mac_input.text().strip()
        if not new_mac or not self.validate_mac(new_mac):
            self.status_label.setText("Enter a valid MAC address (format: XX:XX:XX:XX:XX:XX).")
            return
        try:
            self.mac_changer.change_mac(net_cfg_id, reg_path, new_mac)
            self.status_label.setText("MAC address changed! Click 'Restart Network' if needed.")
            self.update_current_mac()
        except Exception as e:
            self.status_label.setText(f"Failed to change MAC address: {e}")

    def on_restore(self):
        idx = self.adapter_combo.currentIndex()
        if idx < 0:
            self.status_label.setText("No adapter selected.")
            return
        net_cfg_id, _, reg_path = self.adapters[idx]
        try:
            self.mac_changer.restore_mac(net_cfg_id, reg_path)
            self.status_label.setText("Original MAC address restored! Click 'Restart Network' if needed.")
            self.update_current_mac()
        except Exception as e:
            self.status_label.setText(f"Failed to restore MAC address: {e}")

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

    def validate_mac(self, mac):
        import re
        return re.fullmatch(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", mac) is not None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MacChangerApp()
    window.resize(500, 320)
    window.show()
    sys.exit(app.exec_())