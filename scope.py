from oracle import *

from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Create an oracle object that streams data from the board.
oracle = Oracle()

# Define width of plot (in seconds).
width_in_seconds = 15
dt = 1 / 60

# Plot all the things
plt.close("all")

fig, ax = plt.subplots(figsize=(15, 5))

x = np.arange(0, width_in_seconds, dt)
y = deque(np.zeros_like(x), maxlen=len(x))
line, = ax.plot(x, y)


def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(x))
    return (line,)


def animate(i):
    t_, y_ = oracle.buffer[2].sample
    if y_:
        line.set_ydata(np.sin(x + i / 25))  # update the data.
    return (line,)


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=17, blit=True, save_count=100
)

plt.show()
