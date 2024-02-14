import subprocess, platform
import re

def _windows_handler() -> int:
    list_networks_command: str = 'netsh wlan show networks'
    output: str = subprocess.check_output(list_networks_command, shell=True, text=True)
    matches: list[str] = re.findall("TELLO-\w*", output)

    if (len(matches) > 0):
        command: str = 'netsh wlan connect name={0} ssid={0} interface="Wi-Fi"'.format(matches[0])
        result: subprocess.CompletedProcess[bytes] = subprocess.run(command)
        return result.returncode
    
    return 1

def connect() -> int:
    os_name: str = platform.system()
    if os_name == "Windows":
        return _windows_handler()
    else:
        raise Exception("Unsupported OS")
