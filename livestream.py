from oracle import *

from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from time import time


# Create an oracle object that streams data from the board.
oracle = Oracle()

# Define width of plot (in seconds).
width_in_seconds = 15
dt = 1 / 63

# Plot all the things
plt.close("all")
sns.set_context("poster")
fig, ax = plt.subplots(figsize=(15, 6))
plt.ylim([1000, 1100])

# Set up the line plots.
x = np.arange(-width_in_seconds, 0, dt)
y = deque(np.zeros_like(x), maxlen=len(x))
line, = ax.plot(x, y)
plt.xlabel("Time Relative to Now (seconds)")
plt.ylabel("Bioimpedance (Ohms)")


def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(x))
    return (line,)


def animate(i):
    t_ = True
    while t_:
        t_, y_ = next(oracle.buffer[2].sample)
        if y_:
            y.append(y_)
            line.set_ydata(y)  # update the data.
    return (line,)


# Launch the animation; as long as there is data, the plot will shift to left.
ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=0, blit=True, save_count=100
)

plt.show()
