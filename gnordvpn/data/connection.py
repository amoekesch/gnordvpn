import subprocess

from gnordvpn.data import connectionstatus as cs
from gnordvpn.data import nordvpnexception  as vpnex


class Connection:

    def __init__(self):
        ...


    def open(self, country:str="") -> bool:
        # connect
        if country and country != "":
            stdout = subprocess.run(["nordvpn", "c", country], capture_output=True, text=True).stdout.strip().lower()
        else:
            stdout = subprocess.run(["nordvpn", "c"], capture_output=True, text=True).stdout.strip().lower()

        # eval result
        if "are connected to" in stdout:
            return True
        else:
            raise vpnex.NordVPNException(stdout)


    def close(self) -> bool:
        # disconnect
        stdout = subprocess.run(["nordvpn", "d"], capture_output=True, text=True).stdout

        # eval result
        if "are not connected to" in stdout or "are disconnected" in stdout:
            return True
        else:
            raise vpnex.NordVPNException(stdout)


    def status(self) -> cs.ConnectionStatus:
        # request status
        stdout = subprocess.run(["nordvpn", "status"], capture_output=True, text=True).stdout
        return cs.ConnectionStatus(stdout)