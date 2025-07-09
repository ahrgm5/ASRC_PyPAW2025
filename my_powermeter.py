import pyvisa
from ThorlabsPM100 import ThorlabsPM100
import numpy as np

# import warnings
# warnings.filterwarnings('ignore')
# pip install zeroconf psutil

class PowerMeter():

    def __init__(self):
        """
        A general powermeter interface.
        """

        # self.rm = pyvisa.ResourceManager('@py')
        self.rm = pyvisa.ResourceManager()
        self.powermeters = {}
        self.inst = None
        self.powermeter = None
        self.lastAcq = None
        self.trace = np.zeros(100)
        self.parameters = {"wavelength": None,
                           "background": 0,
                           "unit": None}

        self._str_wavelength = 'sense:corr:wav'
        self._str_power = 'power:dc:unit '

    def find_powermeter(self):
        """Find all available ports with Power Meter: PM100 attached."""
        for addr in self.rm.list_resources():
            try:
                name = self.rm.open_resource(addr).query('*IDN?')
                if 'PM100' in name:
                    self.powermeters[name] = addr
            except:
                pass
        return list(self.powermeters.keys())

    def connect(self, idn):

        """ Connects to the power meter attached to port idn 
            idn example: list(self.powermeters.keys())[0] 
        """
        self.inst = self.rm.open_resource(self.powermeters[idn])
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\r\n'
        self.powermeter = ThorlabsPM100(inst=self.inst)
        self.powermeter.configure.scalar.power()
        self.lastAcq = self.powermeter.read

        self.get_wavelength()
        self.get_unit()

        print('Connected to powermeter: {}'.format(idn))

    def read(self, pure=False, printval=False):
        """ Make measurement: in this case, read power, if 
            pure is False, subtracts the background to the measurement

        """
        if pure:
            val = self.powermeter.read
        else:
            val = self.powermeter.read - self.parameters["background"]
        self.lastAcq = val
        self.trace = np.append(self.trace[1:], val)
        if printval:
            print('Measure: {} {}'.format(val, self.parameters["unit"]))
        return val

    def get_background(self):
        """ Make a background measurement """
        self.parameters["background"] = self.read(pure=True)
        self.read()
        print('Background: {} {}'.format(self.parameters["background"], self.parameters["unit"]))

    def get_wavelength(self):
        """ Get current wavelength used by the power meter""" 
        wl = self.inst.query(self._str_wavelength+'?')
        self.parameters["wavelength"] = wl
        print('Wavelength: {} {}'.format(wl, "nm"))
        return wl

    def set_wavelength(self, wl):
        """ Change wavelength used by the powermeter to calculate the power"""
        self.inst.write(self._str_wavelength+' '+str(int(wl)))
        return self.get_wavelength()

    def get_unit(self):
        """ Get current unit used by the power meter""" 
        u = self.powermeter.sense.power.dc.unit
        self.parameters["unit"] = u     
        return u 

    def set_unit(self, unit):
        """ Set units of the power meter, allowed units: W or dBm"""
        if unit not in ['W', 'dBm']:
            print("Unit must be W or dBm")
        else:
            self.inst.write(self._str_power+unit)
        return self.get_unit()

    def switch_unit(self):
        """ Switch units of powermeter between dBm and W"""
        if self.parameters["unit"] == 'W':
            self.inst.write(self._str_power+'dBm')
        else:
            self.inst.write(self._str_power+'W')
        return self.get_unit()   





# if __name__ == "__main__":    

#     # Initialize class, find powermeters and connect to first one             
#     pm = PowerMeter()
#     lpm = pm.find_powermeter()
#     pm.connect(lpm[0])

#     #Measure, get background and measure again
#     pm.read(printval=True)
#     pm.get_background()
#     pm.read(printval=True)
#     pm.get_wavelength()
#     pm.switch_unit()
#     pm.read(printval=True)
#     pm.switch_unit()
#     pm.read(printval=True)
#     print(lpm)