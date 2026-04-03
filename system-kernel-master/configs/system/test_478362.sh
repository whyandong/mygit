#!/bin/bash
mkdir /usr/share/bluetooth
touch /usr/share/bluetooth/bluetoothd.conf
echo '[General]' > /usr/share/bluetooth/bluetoothd.conf
echo 'OParameter=--noplugin=input' >> /usr/share/bluetooth/bluetoothd.conf