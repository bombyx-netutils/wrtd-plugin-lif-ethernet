#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import struct
import socket
import fcntl


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

    def init2(self, instanceName, cfg, brname, tmpDir):
        assert instanceName == ""
        self.brname = brname

    def start(self):
        pass

    def stop(self):
        pass

    def interface_appear(self, ifname):
        if ifname.startswith("en"):
            _Util.ifUp(ifname)
            _Util.addInterfaceToBridge(self.brname, ifname)
            return True
        else:
            return False

    def interface_disappear(self, ifname):
        pass


class _Util:

    @staticmethod
    def ifUp(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ifreq = struct.pack("16sh", ifname, 0)
            ret = fcntl.ioctl(s.fileno(), 0x8913, ifreq)
            flags = struct.unpack("16sh", ret)[1]                   # SIOCGIFFLAGS
            flags |= 0x1
            ifreq = struct.pack("16sh", ifname, flags)
            fcntl.ioctl(s.fileno(), 0x8914, ifreq)                  # SIOCSIFFLAGS
        finally:
            s.close()

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
