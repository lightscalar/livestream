# Livestream Data into Python

The `livestream.py` script demonstrates real-time plotting of data via
Matplotlib. This code is currently designed to work with a very specific piece
of hardware, but the methods implemented here are pretty general.

Once connected to your favorite Biomonitor device, visualize the live data by
running:

```unix
$/> python livestream.py
```

You can pass a few arguments to this script to change the width of the plot, or
the maximum and minimum y-scale ranges, turn auto-scaling on and off, and set
the number of filter taps. For example, to set the upper limit of the plot to
1500:

```unix
$/> python livestream.py --max 1500
```

To see all available options, run:

```unix
$/> python livestream.py -h

usage: livestream.py [-h] [-w [WIDTH]] [-m [MIN]] [-x [MAX]] [-f [FILTER]]
                     [-c [CHANNEL]] [-a [AUTOSCALE]] [-s [SAVE]]

Visualize data.

optional arguments:
  -h, --help            show this help message and exit
  -w [WIDTH], --width [WIDTH]
                        Width of the plot, in seconds.
  -m [MIN], --min [MIN]
                        Minimum y-scale of plot (Ohms).
  -x [MAX], --max [MAX]
                        Maximum y-scale of plot (Ohms).
  -f [FILTER], --filter [FILTER]
                        Number of filter taps to use; 0 for no filtering.
  -c [CHANNEL], --channel [CHANNEL]
                        Which channel should we plot?
  -a [AUTOSCALE], --autoscale [AUTOSCALE]
                        Autoscale on (1) or off (0)
  -s [SAVE], --save [SAVE]
                        Save the data to disk (1) or not (0)
```

If the `-s` flag is set to `1`, data will be written to the disk in the `/data`
folder. This data can later be visualized and filtered by running the
`view_data.py` script.
