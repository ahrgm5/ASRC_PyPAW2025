import json
import glob
import numpy as np
import matplotlib.pyplot as plt

# find the file containig the data
filenames = glob.glob("out*json")
print(filenames)

# open the file and get the data
with open(filenames[-1], "r") as f:
    data = json.load(f)

# check what is in the file
print(data.keys())

# treat the data if necessary
y = np.array(data["measurements"])
y *= 1000 # scale to change units, plot looks better

# factor = y[0]           # remove background if necessary
# y = (y - factor)*1000

# make a nice plot for the data
plt.rcParams.update({'font.size': 15})
fig, ax = plt.subplots(figsize=(8,8))
ax.plot(data["positions"], y, label="Step = {} mm".format(data["parameters"]["step"]))
ax.legend()
ax.set_xlabel("Position (mm)")
ax.set_ylabel("Power (mW)")
ax.tick_params(axis='both', direction='in', top=True, right=True)

# show the plot or save it into a file
#plt.show()
plt.savefig("my_plot_{}.png".format(data["parameters"]["step"]))
