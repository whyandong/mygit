#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import dbus



bus = dbus.SystemBus()

enp2s0 = bus.get_object('org.freedesktop.NetworkManager',
                      '/org/freedesktop/NetworkManager/Devices/enp2s0')

props = enp2s0.getProperties(dbus_interface='org.freedesktop.NetworkManager.Devices')