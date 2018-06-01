# Livestream Data into Python

The `livestream.py` script demonstrates real-time plotting of data via
Matplotlib. This code is currently designed to work with a very specific piece
of hardware, but the methods implemented here are pretty general.

Once connected to your favorite Biomonitor device, visualize the live data by
running:

```unix
$/>python livestream.py
```

You can pass a few arguments to this script to change the width of the plot, or
the maximum and minimum y-scale ranges. For example, to set the upper limit of the plot
to 1500:

```unix
$/>python livestream.py --max 1500
```

To see all available options, run:

```unix
$/>python livestream.py -h
usage: livestream.py [-h] [-w [WIDTH]] [-m [MIN]] [-x [MAX]]                                            
Visualize data.                                     

optional arguments:                                 
  -h, --help            show this help message and exit                                                 
  -w [WIDTH], --width [WIDTH]                       
                        Width of the plot, in seconds.                                                  
  -m [MIN], --min [MIN]                             
                        Minimum y-scale of plot (Ohms).                                                 
  -x [MAX], --max [MAX]                             
                        Maximum y-scale of plot (Ohms).  
```
