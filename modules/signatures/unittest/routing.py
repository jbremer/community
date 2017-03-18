# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import requests

from .abstracts import NamedUnittest

class ConnectLocal(object):
    filter_apinames = "connect",
    should_connect = None

    def check(self):
        connected = False
        for http in self.get_results("network", {}).get("http_ex", []):
            if http["host"] == "localhost":
                connected = True
        for http in self.get_results("network", {}).get("http", []):
            if http["host"] == "localhost":
                connected = True
        return self.should_connect == connected

class ResolveDns(object):
    should_resolve = None

    def check(self):
        for entry in self.get_results("network", {}).get("dns", []):
            if entry["request"] == "cuckoo.sh":
                return bool(entry["answers"]) == self.should_resolve

class RemoteDirect(object):
    filter_apinames = "connect",
    should_connect = None

    def check(self):
        connected = False
        for http in self.get_results("network", {}).get("http_ex", []):
            if http["host"] == "cuckoo.sh":
                connected = True
        for http in self.get_results("network", {}).get("http", []):
            if http["host"] == "cuckoo.sh":
                connected = True
        return self.should_connect == connected

class Myip(object):
    def ipaddr(self):
        for http in self.get_results("network", {}).get("http_ex", []):
            if http["host"] == "myip.cuckoo.sh":
                return open(http["resp"]["path"], "rb").read().strip()

class NormalRoutingUnittest(NamedUnittest):
    description = (
        "In default routing internal traffic is allowed and external "
        "traffic is not allowed."
    )

class DropRoutingUnittest(NamedUnittest):
    description = "In drop routing mode no traffic is allowed at all"

class InternetRoutingUnittest(NamedUnittest):
    description = "In internet routing mode dirty line traffic is allowed"

class TorRoutingUnittest(NamedUnittest):
    description = "In tor routing mode traffic is routed through Tor"

class VPNRoutingUnittest(NamedUnittest):
    description = "In VPN routing mode traffic is routed through a VPN"

class NormalRoutingConnectLocal(ConnectLocal, NormalRoutingUnittest):
    name = "unittest.named.routing.normal.connect-local"
    should_connect = True

class DropRoutingConnectLocal(ConnectLocal, DropRoutingUnittest):
    name = "unittest.named.routing.drop.connect-local"
    should_connect = False

class InternetRoutingConnectLocal(ConnectLocal, InternetRoutingUnittest):
    name = "unittest.named.routing.internet.connect-local"
    should_connect = False

class TorRoutingConnectLocal(ConnectLocal, TorRoutingUnittest):
    name = "unittest.named.routing.tor.connect-local"
    should_connect = False

class VPNRoutingConnectLocal(ConnectLocal, VPNRoutingUnittest):
    name = "unittest.named.routing.vpn.connect-local"
    should_connect = False

class NormalRoutingResolveDns(ResolveDns, NormalRoutingUnittest):
    name = "unittest.named.routing.normal.resolve-dns"
    should_resolve = False

class DropRoutingResolveDns(ResolveDns, DropRoutingUnittest):
    name = "unittest.named.routing.drop.resolve-dns"
    should_resolve = False

class InternetRoutingResolveDns(ResolveDns, InternetRoutingUnittest):
    name = "unittest.named.routing.internet.resolve-dns"
    should_resolve = True

class TorRoutingResolveDns(ResolveDns, TorRoutingUnittest):
    name = "unittest.named.routing.tor.resolve-dns"
    should_resolve = True

class VPNRoutingResolveDns(ResolveDns, VPNRoutingUnittest):
    name = "unittest.named.routing.vpn.resolve-dns"
    should_resolve = True

class NormalRoutingRemoteDirect(RemoteDirect, NormalRoutingUnittest):
    name = "unittest.named.routing.normal.remote-direct"
    should_connect = False

class DropRoutingRemoteDirect(RemoteDirect, DropRoutingUnittest):
    name = "unittest.named.routing.drop.remote-direct"
    should_connect = False

class InternetRoutingRemoteDirect(RemoteDirect, InternetRoutingUnittest):
    name = "unittest.named.routing.internet.remote-direct"
    should_connect = True

class TorRoutingRemoteDirect(RemoteDirect, TorRoutingUnittest):
    name = "unittest.named.routing.tor.remote-direct"
    should_connect = True

class VPNRoutingRemoteDirect(RemoteDirect, VPNRoutingUnittest):
    name = "unittest.named.routing.vpn.remote-direct"
    should_connect = True

class NormalRoutingMyip(Myip, NormalRoutingUnittest):
    name = "unittest.named.routing.normal.myip"

    def check(self):
        return self.ipaddr() is None

class DropRoutingMyip(Myip, DropRoutingUnittest):
    name = "unittest.named.routing.drop.myip"

    def check(self):
        return self.ipaddr() is None

class InternetRoutingMyip(Myip, InternetRoutingUnittest):
    name = "unittest.named.routing.internet.myip"

    def check(self):
        ipaddr = requests.get("http://myip.cuckoo.sh/").content.strip()
        return self.ipaddr() == ipaddr

class TorRoutingMyip(Myip, TorRoutingUnittest):
    name = "unittest.named.routing.tor.myip"

    # Populated once.
    _ipaddrs = []

    def ipaddrs(self):
        if not self._ipaddrs:
            r = requests.get("https://check.torproject.org/exit-addresses")
            for line in r.content.split("\n"):
                if not line.startswith("ExitAddress"):
                    continue
                self._ipaddrs.append(line.split()[1])
        return self._ipaddrs

    def check(self):
        return self.ipaddr() in self.ipaddrs()

class VPNRoutingMyip(Myip, VPNRoutingUnittest):
    name = "unittest.named.routing.vpn.myip"

    def check(self):
        ipaddr = requests.get("http://myip.cuckoo.sh/").content.strip()
        return self.ipaddr() == ipaddr
