import sys
import gi
import ui.gnordvpnwindow as gui
import ui.gnordvpnabout as about

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio
from gi.repository import Adw
from gi.repository import GLib


class GNordVPNApplication(Adw.Application):
    APP_ID = "de.moekesch.gnordvpn"
    APP_NAME = "GNordVPN"
    APP_VERSION = "0.0.1"


    def __init__(self):
        super().__init__(application_id=self.APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        GLib.set_application_name(self.APP_NAME)
        GLib.set_prgname(self.APP_ID)

        # init properties
        self._window = None

        # register shortcuts
        self.create_action("quit", lambda *_: self.quit(), ["<Primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)


    @property
    def window(self):
        return self._window


    def do_activate(self):
        # create and show the window
        self._window = self.props.active_window
        if not self._window:
            self._window = gui.GNordVPNWindow(self.APP_NAME, application=self)
        self._window.present()


    def on_about_action(self, widget, _):
        dialog = about.GNordVPNAbout(self._window, self.APP_ID, self.APP_NAME, self.APP_VERSION)
        dialog.show()


    def on_preferences_action(self, widget, _):
        self._window.show_settings()


    def create_action(self, name, callback, shortcuts=None):
        # create an app action
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main():
    # launch the application
    app = GNordVPNApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()