from filters import *
from vessel import Vessel

from glob import glob
import numpy as np
import pylab as plt
import seaborn as sns


# List all collected data files.
datafiles = glob("data/*.dat")
datafiles = sorted(datafiles)

# Locate and load the latest datafile.
datafile = datafiles[-1]  # grab the latest
v = Vessel(datafile)

t, x = v.t, v.x
t = np.array(t)
x = np.array(x)
t -= t[0]

# Filter the data.
x_, _ = lowpass(t, x, freq_cutoff=3)

plt.ion()
plt.close('all')
plt.figure(100)
plt.plot(t[100:], x_[100:])
