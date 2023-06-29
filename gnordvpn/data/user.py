import subprocess

from gnordvpn.data import nordvpnexception as vpnex


class User:
    def __init__(self):
        # initialize defaults
        self._has_service = False
        self._logged_in = False
        self._valid_account()


    @property
    def has_service(self) -> bool:
        return self._has_service


    @property
    def logged_in(self) -> bool:
        return self._logged_in


    def login(self) -> str:
        # check if already logged in
        if self._logged_in:
            raise vpnex.NordVPNException("You are already logged into your account.")

        # retrieve login URL
        stdout = subprocess.run(["nordvpn", "login", "--nordaccount"], capture_output=True, text=True).stdout.strip().lower()
        if "https" not in stdout:
            raise vpnex.NordVPNException("NordVPN does not accept logins at the moment. Please try again later.")

        # extract and return login URL
        return stdout[stdout.index("https"):].strip()


    def _valid_account(self):
        # retrieve account details
        stdout = subprocess.run(["nordvpn", "account"], capture_output=True, text=True).stdout.strip().lower()

        # eval login status
        self._logged_in = "not logged in" not in stdout
        if not self._logged_in:
            return

        # eval active account
        self._has_service = "service" in stdout and "active" in stdout
        if not self._has_service:
            return

