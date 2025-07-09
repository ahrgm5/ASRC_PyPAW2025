import matplotlib.pyplot
print("PASS: matplotlib")

import numpy
print("PASS: numpy")

import scipy
print("PASS: scipy")

import usb
test_usb  = []
for dev in usb.core.find(find_all=True):
    test_usb.append(dev)
assert len(test_usb) > 0
print("PASS: libusb")

import elliptec
assert hasattr(elliptec, 'devices')
test_elliptec = elliptec.devices
assert len(test_elliptec) > 0
print("PASS: elliptec")

import pyvisa
assert hasattr(pyvisa, 'ResourceManager')
rm = pyvisa.ResourceManager()
print("PASS: PyVISA")

from ThorlabsPM100 import ThorlabsPM100
test_pm = []
for addr in rm.list_resources():
    try:
        name = rm.open_resource(addr).query('*IDN?')
        if 'PM100' in name:
            test_pm.append(addr)
    except:
        pass
assert len(test_pm) > 0
inst = rm.open_resource(test_pm[0])
inst.read_termination = '\n'
inst.write_termination = '\r\n'
powermeter = ThorlabsPM100(inst=inst)
print("PASS: ThorlabsPM100")

import PyQt5
print("PASS: PyQt5")
print("PASS: check Designer")