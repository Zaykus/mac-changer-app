import os
import json
from typing import Dict, Any

class Settings:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.defaults = {
            "theme": "dark",
            "language": "en",
            "window_size": (540, 340),
            "save_position": True,
            "mac_history_size": 10,
            "enable_logging": True,
            "log_level": "INFO"
        }
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as f:
                return {**self.defaults, **json.load(f)}
        except (FileNotFoundError, json.JSONDecodeError):
            return self.defaults.copy()

    def save_settings(self) -> None:
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key: str) -> Any:
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self.save_settings()
