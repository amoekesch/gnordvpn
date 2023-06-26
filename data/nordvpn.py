import subprocess
import re

import data.nordvpnexception as vpnex


class NordVPN:
    REQUIRED_VERSION = 3.16
    _installed_version = "0"

    def __init__(self):
        ...


    @property
    def installed_version(self) -> str:
        return str(self._installed_version)


    def valid_binary(self) -> bool:
        # run NordVPN version command to see if binary exists
        try:
            stdout = subprocess.run(["nordvpn", "-v"], capture_output=True, text=True).stdout.strip().lower()
        except Exception:
            return False

        # all checks passed
        return True


    def valid_version(self) -> bool:
        # retrieve NordVPN version
        stdout = subprocess.run(["nordvpn", "-v"], capture_output=True, text=True).stdout.strip().lower()

        # extract and convert to numeric
        version = stdout[stdout.rindex(" ") + 1:].strip()
        version = version[0:version.rindex(".")].strip()
        self._installed_version = version

        # evaluate version
        if float(version) < self.REQUIRED_VERSION:
            return False

        # all checks passed
        return True


    def list_countries(self) -> list:
        countries = []
        stdout = subprocess.run(["nordvpn", "countries"], capture_output=True, text=True).stdout.strip()
        country_list = re.split(r"[ ]{1,}|\n", stdout, flags=re.MULTILINE)
        for country in sorted(country_list):
            if len(country.strip()) > 1:
                countries.append(country.replace(",", "").strip())

        return countries


    def list_groups(self) -> list:
        groups = []
        stdout = subprocess.run(["nordvpn", "groups"], capture_output=True, text=True).stdout.strip()
        group_list = re.split(r"[ ]{1,}|\n", stdout, flags=re.MULTILINE)
        for group in sorted(group_list):
            if len(group.strip()) > 1:
                groups.append(group.replace(",", "").strip())

        return groups