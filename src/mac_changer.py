import random
import re
import subprocess
import winreg

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

    def disable_enable_adapter(self, net_cfg_id):
        """Disable and enable the network adapter using PowerShell."""
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