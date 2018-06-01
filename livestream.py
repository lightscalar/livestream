from oracle import *

import argparse
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
from time import time


# Check for arguments.
parser = argparse.ArgumentParser(description="Visualize data.")
parser.add_argument(
    "-w",
    "--width",
    nargs="?",
    default=15,
    type=float,
    help="Width of the plot, in seconds.",
)
parser.add_argument(
    "-m",
    "--min",
    nargs="?",
    default=800,
    type=float,
    help="Minimum y-scale of plot (Ohms).",
)
parser.add_argument(
    "-x",
    "--max",
    nargs="?",
    default=1100,
    type=float,
    help="Maximum y-scale of plot (Ohms).",
)
args = parser.parse_args()

# Create an oracle object that streams data from the board.
oracle = Oracle()

# Define width of plot (in seconds).
width_in_seconds = args.width
dt = 1 / 63
min_ohms = args.min
max_ohms = args.max

# Plot all the things
plt.close("all")
sns.set_context("poster")
fig, ax = plt.subplots(figsize=(15, 6))
plt.ylim([min_ohms, max_ohms])

# Set up the line plots.
x = np.arange(-width_in_seconds, 0, dt)
y = deque(np.zeros_like(x), maxlen=len(x))
line, = ax.plot(x, y)
plt.xlabel("Time Relative to Now (seconds)")
plt.ylabel("Bioimpedance (Ohms)")


def init():
    """Only required for blitting to give a clean slate."""
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


# Launch the animation; as long as there is more data available, the plot shifts left.
ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=1, blit=True, save_count=100
)

plt.show()
