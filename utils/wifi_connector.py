"""Module for automatically connecting to Tello WiFi"""

from platform import system as platform_system
from re import findall
from subprocess import CompletedProcess
from subprocess import call as subprocess_call
from subprocess import check_output
from subprocess import run as subprocess_run

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed


def _windows_handler() -> int:
    """Use netsh to discover and connect to the Tello WiFi"""
    list_networks_command: str = "netsh wlan show networks"
    output: str = check_output(list_networks_command, shell=True, text=True)
    matches: list[str] = findall("TELLO-\\w*", output)

    if len(matches) > 0:
        command: str = (
            f'netsh wlan connect name={matches[0]} ssid={matches[0]} interface="Wi-Fi"'
        )
        result: CompletedProcess[bytes] = subprocess_run(command, check=False)
        return result.returncode

    return 1


def _linux_handler() -> int:
    """Use nmcli to discover and connect to the Tello WiFi"""
    list_networks_command: str = "nmcli dev wifi"
    output: str = check_output(list_networks_command, shell=True, text=True)
    matches: list[str] = findall("TELLO-\\w*", output)

    if len(matches) > 0:
        return subprocess_call(["nmcli", "d", "wifi", "connect", matches[0]])

    return 1


def raise_connection_error(_):
    """Raise a ConnectionError"""
    raise ConnectionError(
        "Could not connect to Tello WiFi. Please ensure that the Tello Drone is powered on and broadcasting its WiFi network."
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_result(lambda x: x != 0),
    retry_error_callback=raise_connection_error,
)
def connect_to_wifi() -> int:
    """Attempt to connect to the Tello WiFi. Returns 0 if successful, non-zero if not."""
    os_name: str = platform_system()

    if os_name == "Windows":
        return _windows_handler()

    if os_name == "Linux":
        return _linux_handler()

    return 1
