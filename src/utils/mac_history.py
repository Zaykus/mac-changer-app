import json
import os
from datetime import datetime
from typing import List, Dict

class MacHistory:
    def __init__(self):
        self.history_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "mac_history.json"
        )
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        self.history = self.load_history()

    def load_history(self) -> Dict[str, List[Dict]]:
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_entry(self, adapter_id: str, old_mac: str, new_mac: str) -> None:
        if adapter_id not in self.history:
            self.history[adapter_id] = []
            
        entry = {
            "timestamp": datetime.now().isoformat(),
            "old_mac": old_mac,
            "new_mac": new_mac
        }
        
        self.history[adapter_id].append(entry)
        self.save_history()

    def get_history(self, adapter_id: str) -> List[Dict]:
        return self.history.get(adapter_id, [])

    def get_latest(self, adapter_id: str) -> Dict:
        """Get the most recent MAC change for an adapter."""
        history = self.get_history(adapter_id)
        return history[-1] if history else {}

    def clear_history(self, adapter_id: str = None) -> None:
        """Clear history for specific adapter or all adapters."""
        if adapter_id:
            self.history.pop(adapter_id, None)
        else:
            self.history.clear()
        self.save_history()

    def save_history(self) -> None:
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
