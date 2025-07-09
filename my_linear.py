import elliptec
import sys, os
import time
import save_data

class LinearStage():
    """ Linear stage interface"""

    def __init__(self):
        self.ports = None
        self.devices = None
        self._controller = None
        self.device = None
        self.current_position = None


    def find_devices(self):
        """ Lists serial port names """

        ports = elliptec.scan.find_ports()
        self.ports = ports[:]    
        return ports

    def connect(self, idn):
        self._controller = elliptec.Controller(idn, debug=False)
        self._controller.port = idn
        self.devices = elliptec.scan_for_devices(controller=self._controller)
        self.device = elliptec.Linear(self._controller)
        self.current_position = self.check_position()
        return self.device.info


    def home(self):
        sys.stdout = open(os.devnull, 'w')
        self.device.home()
        sys.stdout = sys.__stdout__


    def move(self, pos):
        sys.stdout = open(os.devnull, 'w')
        position = self.device.set_distance(pos)
        sys.stdout = sys.__stdout__
        self.current_position = position
        return position


    def check_position(self):
        return self.device.get_distance()


    def jog_and_measure(self, start=0, end=60, step=1, function=None, time_wait=1):

        if not function:
            print("Need funcion")
            return 1

        position, measure = [], []
        
        for pos in range(start, end+1, step):
            position.append(self.move(pos))
            measure.append(function())
            time.sleep(time_wait)

        save_data.with_print(position=position, measure=measure, parameters={"step":step})
        return 0





# if __name__ == "__main__":

#     ls = LinearStage()
#     lls = ls.find_devices()
#     info = ls.connect(lls[0])
#     print(info)

#     ls.home()
#     ls.jog_and_measure(step = 5, function=time.time, time_wait=0)
#     ls.move(14)