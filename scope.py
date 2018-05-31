from oracle import *

from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time


# Create an oracle object that streams data from the board.
oracle = Oracle()

# Define width of plot (in seconds).
width_in_seconds = 15
dt = 1 / 60

# Plot all the things
plt.close("all")

fig, ax = plt.subplots(figsize=(15, 5))
plt.ylim([1000, 1100])

x = np.arange(0, width_in_seconds, dt)
y = deque(np.zeros_like(x), maxlen=len(x))
line, = ax.plot(x, y)


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


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=0, blit=True, save_count=100
)

plt.show()
