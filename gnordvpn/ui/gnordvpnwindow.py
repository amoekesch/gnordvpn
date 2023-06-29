import os
import gi
import threading
import time

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gnordvpn.data import connection as cn
from gnordvpn.data import user as user
from gnordvpn.data import nordvpn as nordvpn
from gnordvpn.data import nordvpnsettings as settings
from gnordvpn.data import nordvpnexception as vpnex


@Gtk.Template(filename=os.path.dirname(__file__) + "/gnordvpnwindow.ui")
class GNordVPNWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GNordVPNWindow'

    # define icons
    script_dir = os.path.dirname(__file__)
    img_dir = os.path.join(script_dir, "../resources/icons/")
    pixbuf_img_insecure = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_dir + "gnordvpn-insecure.svg", 128, 128, True)
    pixbuf_img_secure = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_dir + "gnordvpn-secure.svg", 128, 128, True)
    pixbuf_img_uptime = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_dir + "gnordvpn-uptime.svg", 128, 128, True)
    pixbuf_img_upload = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_dir + "gnordvpn-upload.svg", 128, 128, True)
    pixbuf_img_download = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_dir + "gnordvpn-download.svg", 128, 128, True)
    pixbuf_img_host = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_dir + "gnordvpn-host.svg", 128, 128, True)

    # toasts and banners
    toast_overlay = Gtk.Template.Child()
    banner_settings_connected = Gtk.Template.Child()

    # settings controls
    list_settings = Gtk.Template.Child()
    settings_connection = Gtk.Template.Child()
    settings_security = Gtk.Template.Child()
    settings_other = Gtk.Template.Child()
    cmb_technology = Gtk.Template.Child()
    cmb_protocol = Gtk.Template.Child()
    sw_ipvsix = Gtk.Template.Child()
    sw_obfuscate = Gtk.Template.Child()
    sw_autoconnect = Gtk.Template.Child()
    sw_tpl = Gtk.Template.Child()
    sw_firewall = Gtk.Template.Child()
    sw_killswitch = Gtk.Template.Child()
    sw_analytics = Gtk.Template.Child()
    cmb_technology_spinner = Gtk.Template.Child()
    cmb_protocol_spinner = Gtk.Template.Child()
    sw_ipvsix_spinner = Gtk.Template.Child()
    sw_obfuscate_spinner = Gtk.Template.Child()
    sw_autoconnect_spinner = Gtk.Template.Child()
    sw_tpl_spinner = Gtk.Template.Child()
    sw_firewall_spinner = Gtk.Template.Child()
    sw_killswitch_spinner = Gtk.Template.Child()
    sw_analytics_spinner = Gtk.Template.Child()
    handle_cmb_technology = -1
    handle_cmb_protocol = -1
    handle_sw_ipvsix = -1
    handle_sw_obfuscate = -1
    handle_sw_tpl = -1
    handle_sw_autoconnect = -1
    handle_sw_firewall = -1
    handle_sw_killswitch = -1
    handle_sw_analytics = -1

    # status controls
    ar_status = Gtk.Template.Child()
    ar_host = Gtk.Template.Child()
    ar_uploaded = Gtk.Template.Child()
    ar_downloaded = Gtk.Template.Child()
    ar_uptime = Gtk.Template.Child()

    # image controls
    img_status = Gtk.Template.Child()
    img_host = Gtk.Template.Child()
    img_uploaded = Gtk.Template.Child()
    img_downloaded = Gtk.Template.Child()
    img_uptime = Gtk.Template.Child()

    # button controls
    btn_login = Gtk.Template.Child()
    btn_connect = Gtk.Template.Child()
    btn_connect_label = Gtk.Template.Child()
    btn_connect_spinner = Gtk.Template.Child()

    # list controls
    list_categories = Gtk.Template.Child()
    list_countries = Gtk.Template.Child()

    # views and view stack
    view_switcher = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()

    # action status
    _toggling_connection = False

    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        self._init_ui(title)
        if self._init_status_daemon():
            self._init_settings()

    def _init_ui(self, title):
        # sett title
        self.set_title(title)

        # load images
        self.img_host.set_from_pixbuf(self.pixbuf_img_host)
        self.img_uploaded.set_from_pixbuf(self.pixbuf_img_upload)
        self.img_downloaded.set_from_pixbuf(self.pixbuf_img_download)
        self.img_uptime.set_from_pixbuf(self.pixbuf_img_uptime)

        # register signal listeners
        cfg = settings.NordVPNSettings(False)
        self.handle_cmb_technology = self.cmb_technology.connect("changed", self.save_settings_from_selection, cfg.set_technology, cfg.technology_by_index, self.cmb_technology_spinner, True)
        self.handle_cmb_protocol = self.cmb_protocol.connect("changed", self.save_settings_from_selection, cfg.set_protocol, cfg.protocol_by_index, self.cmb_protocol_spinner, True)
        self.handle_sw_tpl = self.sw_tpl.connect("state-set", self.save_settings, cfg.set_threat_protection, self.sw_tpl_spinner, True)
        self.handle_sw_ipvsix = self.sw_ipvsix.connect("state-set", self.save_settings, cfg.set_ipv6, self.sw_ipvsix_spinner, True)
        self.handle_sw_firewall = self.sw_firewall.connect("state-set", self.save_settings, cfg.set_firewall, self.sw_firewall_spinner, True)
        self.handle_sw_obfuscate = self.sw_obfuscate.connect("state-set", self.save_settings, cfg.set_obfuscate, self.sw_obfuscate_spinner, True)
        self.handle_sw_killswitch = self.sw_killswitch.connect("state-set", self.save_settings, cfg.set_killswitch, self.sw_killswitch_spinner, True)
        self.handle_sw_autoconnect = self.sw_autoconnect.connect("state-set", self.save_settings, cfg.set_autoconnect, self.sw_autoconnect_spinner, True)
        self.handle_sw_analytics = self.sw_analytics.connect("state-set", self.save_settings, cfg.set_analytics, self.sw_analytics_spinner, True)

        # handle button states
        self.btn_connect.set_sensitive(False)

        # assign toggle action
        self.btn_connect.connect("clicked", self._toggle_connection)


    def _init_categories(self, vpn):
        while True:
            child = self.list_categories.get_row_at_index(0)
            if child:
                self.list_categories.remove(child)
            else:
                break

        groups = vpn.list_groups()
        for group in groups:
            row_group = Adw.ActionRow()
            row_group.set_icon_name("go-next-symbolic")
            row_group.set_title(group.replace("_", " "))
            row_group_action = Gtk.Button()
            row_group_action.set_margin_end(10)
            row_group_action.set_margin_top(10)
            row_group_action.set_margin_bottom(10)
            row_group_action.set_label("Connect")
            row_group_action.add_css_class("suggested-action")
            row_group_action.connect("clicked", self._toggle_connection, group)
            row_group.add_suffix(row_group_action)
            self.list_categories.append(row_group)


    def _init_countries(self, vpn):
        while True:
            child = self.list_countries.get_row_at_index(0)
            if child:
                self.list_countries.remove(child)
            else:
                break

        countries = vpn.list_countries()
        for country in countries:
            row_country = Adw.ActionRow()
            row_country.set_icon_name("go-next-symbolic")
            row_country.set_title(country.replace("_", " "))
            row_country_action = Gtk.Button()
            row_country_action.set_margin_end(10)
            row_country_action.set_margin_top(10)
            row_country_action.set_margin_bottom(10)
            row_country_action.set_label("Connect")
            row_country_action.add_css_class("suggested-action")
            row_country_action.connect("clicked", self._toggle_connection, country)
            row_country.add_suffix(row_country_action)
            self.list_countries.append(row_country)


    def _init_settings(self):
        # load settings
        cfg = settings.NordVPNSettings()

        # update controls
        self.cmb_technology.handler_block(self.handle_cmb_technology)
        self.cmb_technology.set_active(cfg.technology_index())
        self.cmb_technology.handler_unblock(self.handle_cmb_technology)

        self.cmb_protocol.handler_block(self.handle_cmb_protocol)
        self.cmb_protocol.set_active(cfg.protocol_index())
        self.cmb_protocol.handler_unblock(self.handle_cmb_protocol)

        self.sw_ipvsix.handler_block(self.handle_sw_ipvsix)
        self.sw_ipvsix.set_active(cfg.ipv6)
        self.sw_ipvsix.handler_unblock(self.handle_sw_ipvsix)

        self.sw_obfuscate.handler_block(self.handle_sw_obfuscate)
        self.sw_obfuscate.set_active(cfg.obfuscate)
        self.sw_obfuscate.handler_unblock(self.handle_sw_obfuscate)

        self.sw_autoconnect.handler_block(self.handle_sw_autoconnect)
        self.sw_autoconnect.set_active(cfg.autoconnect)
        self.sw_autoconnect.handler_unblock(self.handle_sw_autoconnect)

        self.sw_tpl.handler_block(self.handle_sw_tpl)
        self.sw_tpl.set_active(cfg.threat_protection)
        self.sw_tpl.handler_unblock(self.handle_sw_tpl)

        self.sw_firewall.handler_block(self.handle_sw_firewall)
        self.sw_firewall.set_active(cfg.firewall)
        self.sw_firewall.handler_unblock(self.handle_sw_firewall)

        self.sw_killswitch.handler_block(self.handle_sw_killswitch)
        self.sw_killswitch.set_active(cfg.killswitch)
        self.sw_killswitch.handler_unblock(self.handle_sw_killswitch)

        self.sw_analytics.handler_block(self.handle_sw_analytics)
        self.sw_analytics.set_active(cfg.analytics)
        self.sw_analytics.handler_unblock(self.handle_sw_analytics)


    def _init_status_daemon(self) -> bool:
        if self._init_binary() and self._init_user():
            # load server groups and countries
            vpn = nordvpn.NordVPN()
            self._init_categories(vpn)
            self._init_countries(vpn)

            # create a status monitor
            daemon = threading.Thread(target=self._status_monitor, daemon=True)
            daemon.start()
            return True

        return False


    def _init_binary(self) -> bool:
        vpn = nordvpn.NordVPN()
        if not vpn.valid_binary():
            toast = Adw.Toast(title="Please install the latest version of NordVPN first.")
            self.toast_overlay.add_toast(toast)
            self.img_status.set_from_pixbuf(self.pixbuf_img_insecure)
            return False

        if not vpn.valid_version():
            required_version = str(vpn.REQUIRED_VERSION)
            toast = Adw.Toast(title=f"Please install the current version of NordVPN (min. {required_version}).")
            self.toast_overlay.add_toast(toast)
            self.img_status.set_from_pixbuf(self.pixbuf_img_insecure)
            return False

        return True


    def _init_user(self) -> bool:
        usr = user.User()
        if not usr.logged_in:
            self.img_status.set_from_pixbuf(self.pixbuf_img_insecure)
            try:
                # retrieve URL and notify users
                self.btn_login.set_uri(usr.login())
            except vpnex.NordVPNException as ex:
                toast = Adw.Toast(title=ex)
                self.toast_overlay.add_toast(toast)
                return False
            # start login monitor
            daemon = threading.Thread(target=self._login_monitor, daemon=True)
            daemon.start()
            # update UI
            self.btn_login.set_visible(True)
            toast = Adw.Toast(title=f"Please log into your NordVPN account first.")
            self.toast_overlay.add_toast(toast)
            return False

        if not usr.has_service:
            self.img_status.set_from_pixbuf(self.pixbuf_img_insecure)
            toast = Adw.Toast(title=f"To use the app, please buy a valid NordVPN service package first.")
            self.toast_overlay.add_toast(toast)
            return False

        return True


    def show_settings(self):
        self.view_stack.set_visible_child_name("page_settings")


    def save_settings_from_selection(self, widget, func, idx_func, spinner, *args):
        # retrieve value
        idx = widget.get_active()
        val = idx_func(idx)
        self.save_settings(widget, val, func, spinner, *args)

    def save_settings(self, widget, val, func, spinner, *args):
        # disable pages
        self.view_switcher.set_view_switcher_enabled(False)
        self.list_settings.set_sensitive(False)
        spinner.set_spinning(True)

        # execute callable to update value
        try:
            func(val, True)
            success = True
        except vpnex.NordVPNException as ex:
            toast_message = str(ex)
            success = False

        # re-initialize settings page and list pages
        self._init_settings()
        vpn = nordvpn.NordVPN()
        self._init_categories(vpn)
        self._init_countries(vpn)

        # re-enable pages
        self.view_switcher.set_view_switcher_enabled(True)
        self.list_settings.set_sensitive(True)
        spinner.set_spinning(False)

        # show errors
        if not success:
            toast = Adw.Toast(title=toast_message)
            self.toast_overlay.add_toast(toast)


    def _login_monitor(self):
        login_complete = False
        while not login_complete:
            # wait for 2 seconds until next update
            time.sleep(2)

            # check again
            usr = user.User()
            login_complete = usr.logged_in

        # start status monitor and load settings
        if login_complete:
            self.btn_login.set_visible(False)
            self._init_status_daemon()
            self._init_settings()

    def _status_monitor(self):
        con = cn.Connection()

        while True:
            if not self._toggling_connection:
                # retrieve status
                status = con.status()

                # update UI
                self.ar_host.set_title(f"{status.host} ({status.country})")
                self.ar_uploaded.set_title(status.uploaded)
                self.ar_downloaded.set_title(status.downloaded)
                self.ar_uptime.set_title(status.uptime)

                if status.connected:
                    self.img_status.set_from_pixbuf(self.pixbuf_img_secure)
                    self.ar_status.set_title(f"Connected ({status.technology} / {status.protocol})")
                    self.ar_status.set_subtitle("Your connection is secure.")
                    self.btn_connect_label.set_label("Disconnect")
                    self.btn_connect.remove_css_class("suggested-action")
                    self.btn_connect.add_css_class("destructive-action")
                    self.banner_settings_connected.set_revealed(True)
                    self.settings_connection.set_sensitive(False)
                    self.settings_security.set_sensitive(False)
                    self.settings_other.set_sensitive(False)
                    self.btn_connect_spinner.set_spinning(False)
                    self.btn_connect.set_sensitive(True)
                else:
                    self.img_status.set_from_pixbuf(self.pixbuf_img_insecure)
                    self.ar_status.set_title("Disconnected")
                    self.ar_status.set_subtitle("Your current connection is not secure.")
                    self.btn_connect_label.set_label("Connect")
                    self.btn_connect.remove_css_class("destructive-action")
                    self.btn_connect.add_css_class("suggested-action")
                    self.banner_settings_connected.set_revealed(False)
                    self.settings_connection.set_sensitive(True)
                    self.settings_security.set_sensitive(True)
                    self.settings_other.set_sensitive(True)
                    self.btn_connect_spinner.set_spinning(False)
                    self.btn_connect.set_sensitive(True)
                    self.list_categories.set_sensitive(True)
                    self.list_countries.set_sensitive(True)

                # wait for 2 seconds until next update
                time.sleep(2)


    def _toggle_connection(self, *args):
        # block UI
        self._toggling_connection = True
        self.btn_connect.set_sensitive(False)
        self.list_categories.set_sensitive(False)
        self.list_countries.set_sensitive(False)
        self.btn_connect.remove_css_class("destructive-action")
        self.btn_connect.remove_css_class("suggested-action")
        self.btn_connect_spinner.set_spinning(True)
        self.view_stack.set_visible_child_name("page_status")
        self.list_countries.set_sensitive(False)

        # define callable
        con = cn.Connection()
        if con.status().connected:
            func = self._toggle_connection_disconnect
        else:
            func = self._toggle_connection_connect

        # start thread to connect
        th = threading.Thread(target=func, args=args, daemon=False)
        th.start()


    def _toggle_connection_connect(self, *args):
        server = "" if len(args) < 2 else args[1]
        con = cn.Connection()
        con.open(server)
        self._toggling_connection = False


    def _toggle_connection_disconnect(self, *args):
        con = cn.Connection()
        con.close()
        self._toggling_connection = False