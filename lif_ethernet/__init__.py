#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import struct
import socket
import fcntl
import pyroute2


def get_plugin_list():
    return [
        "ethernet",
    ]


def get_plugin(name):
    if name == "ethernet":
        return _PluginObject()
    else:
        assert False


class _PluginObject:

    def init2(self, instanceName, cfg, tmpDir):
        assert instanceName == ""

    def start(self):
        pass

    def stop(self):
        pass

    def get_bridge(self):
        return None

    def interface_appear(self, bridge, ifname):
        if ifname.startswith("en"):
            with pyroute2.IPRoute() as ip:
                idx = ip.link_lookup(ifname=ifname)[0]
                ip.link("set", index=idx, state="up")
            _Util.addInterfaceToBridge(bridge.get_name(), ifname)
            return True
        else:
            return False

    def interface_disappear(self, ifname):
        pass


class _Util:

    @staticmethod
    def addInterfaceToBridge(brname, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ifreq = struct.pack("16si", ifname, 0)
            ret = fcntl.ioctl(s.fileno(), 0x8933, ifreq)            # SIOCGIFINDEX
            ifindex = struct.unpack("16si", ret)[1]

            ifreq = struct.pack("16si", brname, ifindex)
            fcntl.ioctl(s.fileno(), 0x89a2, ifreq)                  # SIOCBRADDIF
        finally:
            s.close()
