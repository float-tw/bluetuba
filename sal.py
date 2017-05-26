#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stack Abstraction Layer
from __future__ import absolute_import, print_function, unicode_literals

import gobject

import dbus
import dbus.glib
import dbus.mainloop.glib
import threading

gobject.threads_init()
dbus.glib.threads_init()
dbus.mainloop.glib.threads_init()

class sal(object):
    def __init__(self):
        self.relevant_ifaces = ["org.bluez.Adapter1", "org.bluez.Device1", "org.bluez.MediaTransport1" ]

        dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

        self.bus = dbus.SystemBus()

        self.bus.add_signal_receiver(self.property_changed, bus_name="org.bluez",
                dbus_interface="org.freedesktop.DBus.Properties",
                signal_name="PropertiesChanged",
                path_keyword="path")

        self.bus.add_signal_receiver(self.interfaces_added, bus_name="org.bluez",
                dbus_interface="org.freedesktop.DBus.ObjectManager",
                signal_name="InterfacesAdded")

        self.bus.add_signal_receiver(self.interfaces_removed, bus_name="org.bluez",
                dbus_interface="org.freedesktop.DBus.ObjectManager",
                signal_name="InterfacesRemoved")


    def property_changed(self, interface, changed, invalidated, path):
        iface = interface[interface.rfind(".") + 1:]
        for name, value in changed.iteritems():
            val = str(value)
            print("{%s.PropertyChanged} [%s] %s = %s" % (iface, path, name,
                                        val))

    def interfaces_added(self, path, interfaces):
        for iface, props in interfaces.iteritems():
            if not(iface in self.relevant_ifaces):
                continue
            if iface == "org.bluez.MediaTransport1":
                dev_path = props["Device"]
                obj = self.bus.get_object("org.bluez", dev_path)
                iface = dbus.Interface(obj, "org.freedesktop.DBus.Properties")
                dev_name = iface.Get("org.bluez.Device1", "Name")
                self.connectCB(dev_name)
            print("{Added %s} [%s]" % (iface, path))
            for name, value in props.iteritems():
                print("      %s = %s" % (name, value))

    def interfaces_removed(self, path, interfaces):
        for iface in interfaces:
            if not(iface in self.relevant_ifaces):
                continue
            print("{Removed %s} [%s]" % (iface, path))

    def regConnectCB(self, cb):
        self.connectCB = cb

    def regDisconnectCB(self, cb):
        self.disconnectCB = cb
