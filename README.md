> **Note**
> This application was developed specifically for the GNOME desktop environment. A version suited for KDE built in C++/QT can be found here: [Kompass](https://github.com/amoekesch/Kompass).

# GNordVPN

GNordVPN - Open-source graphical NordVPN client for Linux written in Python using GTK4 and Libadwaita.

![GNordVPN Connected](https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/connected.png)

## Table of Contents

* [About](#About)
* [Features](#Features)
* [Usage](#Usage)
* [Installation](#Installation)
* [Gallery](#Gallery)
* [Dependencies](#Dependencies)
* [Attribution](#Attribution)

## About

**What is GNordVPN?** GNordVPN is an easy-to-use graphical user interface (GUI) wrapping the core functionality provided by NordVPN Linux command-line interface (CLI).
It relies directly on the NordVPN CLI and provides the most commonly used features in a user-friendly interface.

**What GNordVPN is not!** GNordVPN was never meant to implement all available NordVPN features. It's intention is to provide a quick and easy way to connect to a VPN, disconnect a VPN and show the current VPN status.

Please make sure to install the minimum required NordVPN version ([Dependencies](#Dependencies))
to use this application.

## Features

* Connect to NordVPN
  * Servers by <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/countries.png">Country</a>
  * Servers by <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/groups.png">Category/Group</a>
  * <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/connected.png">Fastest</a> (as suggested by NordVPN)
* Supports all common <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/settings.png">NordVPN settings</a> available on Linux
  * Technology and Protocol
  * Threat Protection
  * KillSwitch
  * Obfuscate
  * Firewall
  * etc.
* **Free** and **open-source**
* **Secure!** The application does ot store your NordVPN credentials.
* **Lightweight!** The application does not need to run while connected to NordVPN.
* Support for **Light** and **Dark** mode

## Usage

**GNordVPN is easy to use.** Select either a specific VPN server type, a country to connect to, or put your fate in the hands of NordVPN and let it decide what is the fastest server to use. Toggle the *Connect* switch and that's it.

![GNordVPN Disconnected](https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/disconnected.png)

As soon as GNordVPN could establish a connection with a VPN server, the user interface will show the connection status and additional connection details:. To *Disconnect* toggle that switch once more and GNordVPN will disconnect you from the VPN.

![GNordVPN Connected](https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/connected.png)

## Installation

An easy-to-install package is **in the works**. Come back soon for more!

## Gallery

<a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/disconnected.png"><img src="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/disconnected.png" width="18%"></img></a> <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/connected.png"><img src="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/connected.png" width="18%"></img></a> <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/groups.png"><img src="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/groups.png" width="18%"></img></a> <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/countries.png"><img src="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/countries.png" width="18%"></img></a> <a target="_blank" href="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/settings.png"><img src="https://github.com/amoekesch/gnordvpn/raw/master/gnordvpn/resources/doc/settings.png" width="18%"></img></a>

## Dependencies

GNordVPN is written in Python using GTK4 and Libadwaita (ADW). It relies heavily on the NordVPN CLI. Here is its full list of dependencies:

* [Python](https://www.python.org/) (v3.9+)
* [GTK4](https://docs.gtk.org/gtk4/) (v4.0+)
* [ADW](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/index.html) (v1.0+)
* [NordVPN CLI](https://nordvpn.com/download/linux/) (v3.16.0+)

## Attribution

* [SVG Repo](https://www.svgrepo.com/) - Custom application icons built on SVG icons from SVG Repo