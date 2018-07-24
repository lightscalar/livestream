"""A class for stashing data (and possibly filtering it, in an online way)."""
import numpy as np
from collections import deque


class Stash(object):
    """Store data and filter it."""

    def __init__(self, nb_taps=5, demand_uniqueness=True, do_filter=True):
        self.do_filter = do_filter
        self.demand_uniqueness = demand_uniqueness
        self.M = M = nb_taps
        self.p = p = int((M - 1) / 2)
        self.q = p + 1

        # These vectors hold the time/values being added to the stash.
        self.x = deque([], maxlen=1000)
        self.t = deque([], maxlen=1000)

        # These variables are the filtered version of t/x; cannot sample from these vectors...
        self.t_ = deque([], maxlen=1000)
        self.x_ = deque([], maxlen=1000)
        self.x_prev = 0

        # These variables are the filtered version from which we sample.  We
        # have two versions because, depending on how quickly we're sampling
        # from the the object, we may exhaust the data needed for the moving
        # average filter.
        self.t_filtered = deque([], maxlen=1000)
        self.x_filtered = deque([], maxlen=1000)

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
        if len(self.x) >= self.M and self.do_filter:
            self.filter()

    def filter(self):
        """Super efficient moving average filter."""
        M, p, q = self.M, self.p, self.q
        x = self.x
        idx = len(self.x) - (p + 1)
        x_ = self.x_prev + (x[idx + p] - x[idx - q]) / M
        self.t_.append(self.t[idx])
        self.t_filtered.append(self.t[idx])
        self.x_.append(x_)
        self.x_filtered.append(x_)
        self.x_prev = x_

    @property
    def sample(self):
        """Return first observed pair (t, x), still in queue."""
        if self.do_filter:
            if len(self.t_filtered) > 0:
                yield self.t_filtered.popleft(), self.x_filtered.popleft()
            else:
                yield None, None
        else: # let's not filter
            if len(self.t) > 0:
                yield self.t.popleft(), self.x.popleft()
            else:
                yield None, None


if __name__ == "__main__":
    import pylab as plt

    plt.ion()
    plt.close("all")

    # Create a noisy sinusoidal signal.
    t = np.linspace(0, 10, 1000)
    x = np.sin(2 * np.pi * t / 3) + 0.05 * np.random.randn(1000) + 15

    # Estimate number of taps required for specified cutoff frequency.
    # See (https://goo.gl/yCySp4) for more details.
    fs = 100  # sampling rate
    fc = 5  # cutoff frequency
    Fco = fc / fs  # normalized cutoff frequency
    alpha = 0.196202
    N = int(np.ceil(np.sqrt(alpha + Fco ** 2) / Fco))

    # Plot the example data
    plt.figure()
    plt.plot(t, x)

    # Create a data stash!
    pzt = Stash(N)

    # Add a bunch of samples to the stash.
    for t_, x_ in zip(t, x):
        pzt.add(t_, x_)

    # Now plot the resulting filtered data.
    t_, x_ = pzt.t_filtered, pzt.x_filtered
    plt.plot(t_, x_)

    # Note also that you can sample from the object because it's a generator.
    t0, x0 = next(pzt.sample)
    t1, x1 = next(pzt.sample)
    # ... and so on
