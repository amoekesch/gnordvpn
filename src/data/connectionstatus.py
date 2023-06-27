class ConnectionStatus:
    def __init__(self, status):
        # set defaults
        self._connected = False
        self._host = "N/A"
        self._country = "N/A"
        self._technology = "N/A"
        self._protocol = "N/A"
        self._uptime = "00:00:00"
        self._uploaded = "0 bytes"
        self._downloaded = "0 bytes"

        # initialize from status
        self._parse(status)


    @property
    def connected(self) -> bool:
        return self._connected


    @property
    def host(self) -> str:
        return self._host


    @property
    def country(self) -> str:
        return self._country


    @property
    def technology(self) -> str:
        return self._technology


    @property
    def protocol(self) -> str:
        return self._protocol


    @property
    def uploaded(self) -> str:
        return self._uploaded


    @property
    def downloaded(self) -> str:
        return self._downloaded


    @property
    def uptime(self) -> str:
        return self._uptime


    def _parse(self, status):
        # parse actual status
        for line in status.splitlines():
            if ":" in line:
                key, value = line.split(r":")
                if key.strip().lower() == "status" and value.strip().lower() == "connected":
                    self._connected = True
                elif key.strip().lower() == "hostname":
                    self._host = value.strip()
                elif key.strip().lower() == "country":
                    self._country = value.strip()
                elif key.strip().lower().endswith("technology"):
                    self._technology = value.strip()
                elif key.strip().lower().endswith("protocol"):
                    self._protocol = value.strip()
                elif key.strip().lower() == "transfer":
                    self._downloaded, self._uploaded = value.strip().split(r",")
                    self._uploaded = self._uploaded.strip().replace(" sent", "")
                    self._downloaded = self._downloaded.strip().replace(" received", "")
                elif key.strip().lower() == "uptime":
                    uptime_list = value.strip().split(" ")
                    if len(uptime_list) == 2:
                        self._uptime = "00:00:" + uptime_list[0].rjust(2, "0")
                    elif len(uptime_list) == 4:
                        self._uptime = "00:" +  uptime_list[0].rjust(2, "0") + ":" + uptime_list[2].rjust(2, "0")
                    elif len(uptime_list) == 6:
                        self._uptime = uptime_list[0].rjust(2, "0") + ":" +  uptime_list[2].rjust(2, "0") + ":" + uptime_list[4].rjust(2, "0")
                    elif len(uptime_list) == 8:
                        days = int(uptime_list[0])
                        hours = int(uptime_list[2])
                        self._uptime = str((days * 24) + hours).rjust(2, "0") + ":" +  uptime_list[4].rjust(2, "0") + ":" + uptime_list[6].rjust(2, "0")

    def __str__(self) -> str:
        return f"Connected:\t{self._connected}" + \
            f"\nHost:\t\t{self._host}" + \
            f"\nCountry:\t{self._country}" + \
            f"\nTechnology:\t{self._technology}" + \
            f"\nProtocol:\t{self._protocol}" + \
            f"\nUploaded:\t{self._uploaded}" + \
            f"\nDownloaded:\t{self._downloaded}" + \
            f"\nUptime:\t\t{self._uptime}"
