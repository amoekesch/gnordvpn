import subprocess

from gnordvpn.data import nordvpnexception as vpnex


class NordVPNSettings:
    def __init__(self, reload: bool = True):
        # initialize defaults
        self.technologies = { "NORDLYNX": 0, "OPENVPN": 1}
        self.protocols = {"TCP": 0, "UDP": 1}

        self._technology = ""
        self._protocol = "UDP"
        self._analytics = False
        self._ipv6 = False
        self._obfuscate = False
        self._autoconnect = False
        self._threat_protection = False
        self._firewall = False
        self._killswitch = False

        if reload:
            self.init_settingss()


    @property
    def technology(self) -> str:
        return self._technology

    def set_technology(self, technology: str, store: bool = False):
        self._technology = technology
        if store:
            self.save("technology", technology.replace(" ", "").upper())

    def technology_index(self) -> int:
        return self.technologies[self._technology.upper()]

    def technology_by_index(self, idx: int) -> str:
        for key, val in self.technologies.items():
            if val == idx:
                return key
        return -1


    @property
    def protocol(self) -> str:
        return self._protocol

    def set_protocol(self, protocol: str, store: bool = False):
        self._protocol = protocol
        if store:
            self.save("protocol", protocol.replace(" ", "").upper())

    def protocol_index(self) -> int:
        return self.protocols[self._protocol.upper()]

    def protocol_by_index(self, idx: int) -> str:
        for key, val in self.protocols.items():
            if val == idx:
                return key
        return -1


    @property
    def analytics(self) -> bool:
        return self._analytics

    def set_analytics(self, analytics: bool, store: bool = False):
        self._analytics = analytics
        if store:
            val = "enabled" if analytics else "disabled"
            self.save("analytics", val)


    @property
    def ipv6(self) -> bool:
        return self._ipv6

    def set_ipv6(self, ipv6: bool, store: bool = False):
        self._ipv6 = ipv6
        if store:
            val = "enabled" if ipv6 else "disabled"
            self.save("ipv6", val)


    @property
    def obfuscate(self) -> bool:
        return self._obfuscate

    def set_obfuscate(self, obfuscate: bool, store: bool = False):
        self._obfuscate = obfuscate
        if store:
            val = "enabled" if obfuscate else "disabled"
            self.save("obfuscate", val)


    @property
    def autoconnect(self) -> bool:
        return self._autoconnect

    def set_autoconnect(self, autoconnect: bool, store: bool = False):
        self._autoconnect = autoconnect
        if store:
            val = "enabled" if autoconnect else "disabled"
            self.save("autoconnect", val)


    @property
    def threat_protection(self) -> bool:
        return self._threat_protection

    def set_threat_protection(self, threat_protection: bool, store: bool = False):
        self._threat_protection = threat_protection
        if store:
            val = "enabled" if threat_protection else "disabled"
            self.save("tpl", val)


    @property
    def firewall(self) -> bool:
        return self._firewall

    def set_firewall(self, firewall: bool, store: bool = False):
        self._firewall = firewall
        if store:
            val = "enabled" if firewall else "disabled"
            self.save("firewall", val)


    @property
    def killswitch(self) -> bool:
        return self._killswitch

    def set_killswitch(self, killswitch: bool, store: bool = False):
        self._killswitch = killswitch
        if store:
            val = "enabled" if killswitch else "disabled"
            self.save("killswith", val)


    def init_settingss(self) :
        stdout = subprocess.run(["nordvpn", "settings"], capture_output=True, text=True).stdout.strip()
        for setting in stdout.splitlines():
            if ":" in setting:
                key, value = setting.split(r":")
                if key.strip().lower() == "technology":
                    self._technology = value.strip()
                elif key.strip().lower() == "protocol":
                    self._protocol = value.strip()
                elif key.strip().lower() == "firewall":
                    self._firewall = True if value.strip().lower() == "enabled" else False
                elif key.strip().lower() == "kill switch":
                    self._killswitch = True if value.strip().lower() == "enabled" else False
                elif key.strip().lower() == "obfuscate":
                    self._obfuscate = True if value.strip().lower() == "enabled" else False
                elif key.strip().lower() == "threat protection lite":
                    self._threat_protection = True if value.strip().lower() == "enabled" else False
                elif key.strip().lower() == "auto-connect":
                    self._autoconnect = True if value.strip().lower() == "enabled" else False
                elif key.strip().lower() == "ipv6":
                    self._ipv6 = True if value.strip().lower() == "enabled" else False
                elif key.strip().lower() == "analytics":
                    self._analytics = True if value.strip().lower() == "enabled" else False


    def save(self, key: str, value: str):
        # write
        stdout = subprocess.run(["nordvpn", "set", key, value], capture_output=True, text=True).stdout.strip()
        if not "successfully" in stdout.lower():
            raise vpnex.NordVPNException(f"Data ({key}) could not be stored. Try again!")


    def __str__(self) -> str:
        return f"Technology:\t\t\t{self._technology}" + \
            f"\nProtocol:\t\t\t{self._protocol}" + \
            f"\nFirewall:\t\t\t{self._firewall}" + \
            f"\nKill Switch:\t\t{self._killswitch}" + \
            f"\nObfuscate:\t\t\t{self._obfuscate}" + \
            f"\nThreat Protection:\t{self._threat_protection}" + \
            f"\nAuto-Connect:\t\t{self._autoconnect}" + \
            f"\nIPv6:\t\t\t\t{self._ipv6}" + \
            f"\nAnalytics:\t\t\t{self._analytics}"

