"""Module for automatically connecting to Trello WiFi"""

import subprocess
import platform
import re

def _windows_handler() -> int:
    """Use netsh to discover and connect to the Trello WiFi"""
    list_networks_command: str = 'netsh wlan show networks'
    output: str = subprocess.check_output(list_networks_command, shell=True, text=True)
    matches: list[str] = re.findall("TELLO-\\w*", output)

    if len(matches) > 0:
        command: str = f'netsh wlan connect name={matches[0]} ssid={matches[0]} interface="Wi-Fi"'
        result: subprocess.CompletedProcess[bytes] = subprocess.run(command, check=False)
        return result.returncode

    return 1

def connect() -> int:
    """Attempt to connect to the Trello WiFi. Returns 0 if succesfull, non-zero if not"""
    os_name: str = platform.system()

    if os_name == "Windows":
        return _windows_handler()

    return 1
