import random
import re
import subprocess
import winreg
import socket
import json
from typing import Dict, List, Tuple, Optional

class MacChanger:
    def get_adapters(self):
        """Return a list of (name, description, registry_path) for network adapters."""
        adapters = []
        reg_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            for i in range(0, 1000):
                try:
                    subkey_name = f"{i:04}"
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            name = winreg.QueryValueEx(subkey, "NetCfgInstanceId")[0]
                            desc = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                            adapters.append((name, desc, reg_path + "\\" + subkey_name))
                        except FileNotFoundError:
                            continue
                except OSError:
                    break
        return adapters

    def get_current_mac(self, net_cfg_id):
        """Get current MAC address for the adapter with given NetCfgInstanceId."""
        output = subprocess.check_output(
            f'getmac /v /fo list', shell=True, encoding='utf-8', errors='ignore'
        )
        pattern = re.compile(rf'Connection Name:.*\n.*Physical Address: ([\w\-]+).*Device.*{net_cfg_id}', re.DOTALL)
        matches = re.findall(rf'Physical Address: ([\w\-]+)[\s\S]+Transport Name:.*{net_cfg_id}', output)
        if matches:
            return matches[0].replace('-', ':')
        return None

    def generate_random_mac(self):
        """Generate a random MAC address (locally administered, unicast)."""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        mac[0] = (mac[0] & 0b11111110) | 0b00000010  # Locally administered, unicast
        return ':'.join(f"{b:02x}" for b in mac)

    def set_mac_address(self, reg_path, new_mac):
        """Set the NetworkAddress value in the registry."""
        mac_no_colon = new_mac.replace(':', '').replace('-', '')
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, mac_no_colon)

    def reset_mac_address(self, reg_path):
        """Remove the NetworkAddress value from the registry (set to Not Present)."""
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            try:
                winreg.DeleteValue(key, "NetworkAddress")
            except FileNotFoundError:
                pass

    def disable_enable_adapter(self, net_cfg_id):
        """Disable and enable the network adapter using PowerShell (Windows 10/11)."""
        guid = net_cfg_id.strip('{}')
        # Disable adapter
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Get-NetAdapter | Where-Object {{$_.InterfaceGuid -eq '{{{guid}}}'}} | Disable-NetAdapter -Confirm:$false"
            ],
            shell=True
        )
        # Enable adapter
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Get-NetAdapter | Where-Object {{$_.InterfaceGuid -eq '{{{guid}}}'}} | Enable-NetAdapter -Confirm:$false"
            ],
            shell=True
        )

    def change_mac(self, net_cfg_id, reg_path, new_mac):
        """Change the MAC address for the adapter."""
        self.set_mac_address(reg_path, new_mac)
        self.disable_enable_adapter(net_cfg_id)

    def restore_mac(self, net_cfg_id, reg_path):
        """Restore the original MAC address."""
        self.reset_mac_address(reg_path)
        self.disable_enable_adapter(net_cfg_id)

    def restart_adapter(self, net_cfg_id):
        """Restart the network adapter (disable then enable)."""
        self.disable_enable_adapter(net_cfg_id)

    # Added for manual MAC address enable/disable (Value/Not Present)
    def set_manual_mac_enabled(self, reg_path, enabled, mac_value=None):
        """
        Enable or disable manual MAC address.
        If enabled, set to mac_value. If disabled, remove the value ("Not Present").
        """
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            if enabled and mac_value:
                mac_no_colon = mac_value.replace(':', '').replace('-', '')
                winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, mac_no_colon)
            else:
                try:
                    winreg.DeleteValue(key, "NetworkAddress")
                except FileNotFoundError:
                    pass

    def get_adapter_details(self, net_cfg_id: str) -> Dict[str, str]:
        """Get detailed information about the network adapter."""
        guid = net_cfg_id.strip('{}')
        details = {}
        
        # Get adapter info using PowerShell
        ps_command = (
            "Get-NetAdapter | "
            f"Where-Object {{$_.InterfaceGuid -eq '{{{guid}}}'}} | "
            "Select-Object -Property InterfaceDescription, Status, LinkSpeed, MediaType, MacAddress, IPAddress | "
            "ConvertTo-Json"
        )
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                adapter_info = json.loads(result.stdout)
                details = {
                    "Description": adapter_info.get("InterfaceDescription", "Unknown"),
                    "Status": adapter_info.get("Status", "Unknown"),
                    "Speed": adapter_info.get("LinkSpeed", "Unknown"),
                    "Type": adapter_info.get("MediaType", "Unknown"),
                    "MAC": adapter_info.get("MacAddress", "Unknown"),
                    "IP": adapter_info.get("IPAddress", ["Unknown"])[0]
                }
        except Exception as e:
            details = {
                "Error": f"Failed to get adapter details: {str(e)}"
            }
        
        return details

    def save_original_mac(self, net_cfg_id: str, file_path: str = "original_macs.json") -> None:
        """Save the original MAC address to a file."""
        mac = self.get_current_mac(net_cfg_id)
        if mac:
            try:
                with open(file_path, 'r') as f:
                    macs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                macs = {}
            
            macs[net_cfg_id] = mac
            
            with open(file_path, 'w') as f:
                json.dump(macs, f, indent=2)