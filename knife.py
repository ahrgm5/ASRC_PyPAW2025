import matplotlib.pyplot as plt
import my_powermeter as mpm
import my_Linear as mls
import time
import datetime
import save_data
import numpy as np
import glob, json


class KnifeEdge:

    """ Class to perform knife-edge experiment """

    def __init__(self):
        self.powermeter = mpm.PowerMeter()
        self.linear_stage = mls.LinearStage()
        self.parameters = {            # parameters from the linear stage
                            "start": 0,
                            "end":   60,
                            "step":  1, 
                            "sleep": 0.5 
                            }
        self.positions = []
        self.measurements = []

        # First we need to find the devices
        lpm = self.powermeter.find_powermeter()
        lls = self.linear_stage.find_devices()


        # Second, connect to the devices
        try:
            self.powermeter.connect(lpm[0])
        except:
            print("Could not connect to powermeter")
            print(lpm)
            return 

        try:
            self.linear_stage.connect(lls[0])
        except:
            print("Could not connect to linear stage")
            print(lls)
            return


    def initialize(self):
        """ Home the linear stage and measure the backgroung of the powermeter """
        self.linear_stage.home()
        self.powermeter.get_background()

    def get_parameters(self):
        """ Obtain parameters from the linear stage and from the powermeter """
        for key, val in self.parameters.items():
            print("%s: %s" % (key, val))
        for key, val in self.powermeter.parameters.items():
            print("%s: %s" % (key, val))
        return self.parameters, self.powermeter.parameters

    def set_parameters(self, start=0, end=60, step=1, sleep=0, 
                      pm_unit='W', pm_wl=400):
        """ Function to change the experiment parametes """
        self.parameters["start"] = start
        self.parameters["end"] = end
        self.parameters["step"] = step
        self.parameters["sleep"] = sleep

        self.powermeter.set_wavelength(pm_wl)
        self.powermeter.set_unit(pm_unit)
        return self.get_parameters()

    def run(self):
        """ Function to run the experiment itself, creates a file with parametes and the measured values """

        # first get a file name with the current date and time
        filename = "out_"+str(datetime.datetime.now()).replace('.','_').replace(' ', '_').replace(':', '_')

        # loop over the possible positions of the linear stage
        for pos in np.arange(self.parameters["start"], 
                         self.parameters["end"], self.parameters["step"]).tolist():

            # move the stage and store position
            self.positions.append(self.linear_stage.move(pos))
            # measure the power
            self.measurements.append(self.powermeter.read()) 
            # wait for a bit, just in case
            time.sleep(self.parameters["sleep"])

            # save parametes and measurements to file at every iteration, in case there is a crash interruption
            save_data.with_json(filename=filename,
                                parameters=self.parameters, 
                                pm_parameters=self.powermeter.parameters, 
                                positions=self.positions, 
                                measurements=self.measurements)       


exp = KnifeEdge()
exp.initialize()
exp.set_parameters(start = 21, end= 28, step = .5, sleep= .5)
exp.run()
print(exp.__dict__)


filenames = glob.glob("out*json")

with open(filenames[-1], 'r') as f:

    plot = json.load (f)

y = np.array(plot["measurements"])
x = np.array(plot["positions"])

plt.plot(x, y)
plt.show()