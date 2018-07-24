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
parser.add_argument(
    "-f",
    "--filter",
    nargs="?",
    default=3,
    type=float,
    help="Number of filter taps to use; 0 for no filtering.",
)
parser.add_argument(
    "-a",
    "--autoscale",
    nargs="?",
    default=1,
    type=float,
    help="Autoscale on (1) or off (0)",
)
args = parser.parse_args()

# Are we autoscaling?
autoscale = args.autoscale

# Create an oracle object that streams data from the board.
filter_taps = args.filter
oracle = Oracle(nb_taps=filter_taps)

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
    line.set_ydata([0] * len(x))
    return (line,)


def animate(i):
    t_ = True
    while t_:
        t_, y_ = next(oracle.buffer[2].sample)
        if y_:
            y.append(y_)
            line.set_ydata(y)  # update the data.
            mu = np.mean(y)
            std = np.std(y)
            if autoscale:
                plt.ylim([mu - 5 * std, mu + 5 * std])
    return (line,)


# Launch the animation; as long as there is more data available, the plot shifts left.
ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=1, blit=False, save_count=100
)

plt.show()
