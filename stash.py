"""A class for stashing data (and possibly filtering it, in an online way)."""
import numpy as np
from collections import deque


class Stash(object):

    def __init__(self, nb_taps=11, demand_uniqueness=False):
        self.demand_uniqueness = demand_uniqueness
        self.M = M = nb_taps
        self.p = p = int((M - 1) / 2)
        self.q = p + 1
        self.x = deque([], maxlen=1000)
        self.t = deque([], maxlen=1000)
        self.t_ = deque([], maxlen=1000)
        self.y_ = deque([], maxlen=1000)
        self.y_prev = 0

    def add(self, t, x):
        """Add new point."""
        if self.demand_uniqueness:
            # Cannot add two successive identical values.
            if len(self.x) > 0:
                if self.x[-1] != x:
                    self.t.append(t)
                    self.x.append(x)
            else:
                self.t.append(t)
                self.x.append(x)
        else:
            self.t.append(t)
            self.x.append(x)
        if len(self.x) >= self.M:
            self.filter()

    def filter(self):
        """Super efficient moving average filter."""
        M, p, q = self.M, self.p, self.q
        x = self.x
        idx = len(self.x) - (p + 1)
        y_ = self.y_prev + (x[idx + p] - x[idx - q]) / M
        self.t_.append(self.t[idx])
        self.y_.append(y_)
        self.y_prev = y_

    @property
    def sample(self):
        """Return first observed pair (t, y), still in queue."""
        if len(self.t_) > 0:
            yield self.t_.popleft(), self.y_.popleft()
        else:
            yield None, None


if __name__ == "__main__":
    import pylab as plt

    plt.ion()
    plt.close("all")
    t = np.linspace(0, 10, 1000)
    x = np.sin(2 * np.pi * t / 3) + 0.1 * np.random.randn(1000)

    plt.figure()
    plt.plot(t, x)

    # Create a data accumulator.
    pzt = Stash(11)

    for t_, x_ in zip(t, x):
        pzt.add(t_, x_)

    t_, y_ = pzt.t_, pzt.y_
    plt.plot(t_, y_)
