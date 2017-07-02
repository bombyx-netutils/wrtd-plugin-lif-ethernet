#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import struct
import socket
import logging
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

    def init2(self, instanceName, cfg, tmpDir, varDir):
        assert instanceName == ""
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self.intfList = []

    def start(self):
        self.logger.info("Started.")

    def stop(self):
        for ifname in self.intfList:
            self.logger.info("Interface \"%s\" unmanaged." % (ifname))
        self.logger.info("Stopped.")

    def interface_appear(self, bridge, ifname):
        if ifname.startswith("en"):
            with pyroute2.IPRoute() as ip:
                idx = ip.link_lookup(ifname=ifname)[0]
                ip.link("set", index=idx, state="up")
            _Util.addInterfaceToBridge(bridge.get_name(), ifname)
            self.intfList.append(ifname)
            self.logger.info("Interface \"%s\" managed." % (ifname))
            return True
        return False

    def interface_disappear(self, ifname):
        if ifname in self.intfList:
            self.intfList.remove(ifname)
            self.logger.info("Interface \"%s\" unmanaged." % (ifname))


class _Util:

    @staticmethod
    def addInterfaceToBridge(brname, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ifreq = struct.pack("16si", ifname.encode("ascii"), 0)
            ret = fcntl.ioctl(s.fileno(), 0x8933, ifreq)                    # SIOCGIFINDEX
            ifindex = struct.unpack("16si", ret)[1]

            ifreq = struct.pack("16si", brname.encode("ascii"), ifindex)
            fcntl.ioctl(s.fileno(), 0x89a2, ifreq)                          # SIOCBRADDIF
        finally:
            s.close()
