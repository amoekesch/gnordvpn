import gi
import data.nordvpn as vpn

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw
from gi.repository import Gtk


class GNordVPNAbout:
    def __init__(self, parent: Gtk.Widget, app_id: str, app_name: str, app_version: str):
        # init values
        description = f"<b>What is GNordVPN?</b> GNordVPN is an easy-to-use graphical user interface (GUI) wrapping " + \
                      f"the core functionality provided by NordVPN Linux command-line interface (CLI).\nIt relies " + \
                      f"directly on the NordVPN CLI and provides the most commonly used features in a user-friendly " + \
                      f"interface.\n\n" + \
                      f"<b>What GNordVPN is not!</b> GNordVPN was never meant to implement all available NordVPN features. " + \
                      f"It's intention is to provide a quick and easy way to connect to a VPN, disconnect a VPN  " + \
                      f"and show the current VPN status.\n\n" + \
                      f"Please make sure to install at least NordVPN version {vpn.NordVPN.REQUIRED_VERSION} " + \
                      f"to use this application.\n\n"
        contributors = ["SVG Repo https://www.svgrepo.com", "NordVPN https://www.nordvpn.com"]

        # create dialog
        self.dialog = Adw.AboutWindow(transient_for=parent)
        self.dialog.set_application_name(app_name)
        self.dialog.set_version(app_version)
        self.dialog.set_application_icon(app_id)
        self.dialog.set_comments(description)
        self.dialog.set_license_type(Gtk.License(Gtk.License.MIT_X11))
        self.dialog.add_credit_section("Contributors", contributors)
        self.dialog.set_developer_name("Andreas Moekesch")
        self.dialog.set_developers(["Andreas Moekesch"])
        self.dialog.set_website("https://github.com/amoekesch/gnordvpn")
        self.dialog.set_issue_url("https://github.com/amoekesch/gnordvpn/issues")
        self.dialog.set_copyright("© 2023 Andreas Moekesch")


    def show(self):
        self.dialog.present()