from kivy.clock import Clock
from cartesian import *
from collections import deque
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import numpy as np
from time import time, sleep


class TimeSeries(object):

    def __init__(self):
        self.t = np.array([])
        self.v = np.array([])

    def push(self, t, v, dt, chart_width):
        """Add data to the time series."""
        self.t = np.append(self.t, t)
        self.v = np.append(self.v, v)
        self.t -= dt
        idx = np.nonzero(self.t > -chart_width)[0]
        self.t = self.t[idx]
        self.v = self.v[idx]
        return self.t, self.v


class Chart(FloatLayout):
    sensor_name = StringProperty("PZT")
    chart_max = NumericProperty(2.5)
    chart_min = NumericProperty(0.0)
    chart_width = NumericProperty(10)
    data_buffer = ListProperty([])
    buffered = BooleanProperty(False)
    autoscale = BooleanProperty(False)

    def init(self):
        self.ts = TimeSeries()
        self.scaling_buffer = deque([], maxlen=100)
        self.cartesian.init()
        self.chart_min = 0
        self.chart_max = 2.5

    def set_autoscale(self, autoscale):
        # Toggle autoscale.
        self.autoscale = autoscale

    def set_chart_width(self, value):
        # Change chart width (in seconds)
        self.chart_width = value
        self.cartesian.update_axes()

    def set_chart_min(self, value):
        # Adjust chart minimum value
        self.chart_min = value
        self.cartesian.update_axes()

    def set_chart_max(self, value):
        # Adjust chart minimum value
        self.chart_max = value
        self.cartesian.update_axes()

    def add_data(self, data):
        # Add data to the chart's buffer.
        self.data_buffer.extend(data[2])
        if len(self.data_buffer) > 300:
            self.buffered = True

    def tick(self, dt):
        # Update the time series.
        # Sample insertion is probabilistic in order to accommodate possible
        # errors in timing. If delta time is too large, we insert a second
        # sample with probability proportional to the timing error.
        if self.buffered:
            # Ratio of actual to expected delta time:
            ratio = 100 * dt
            excess = ratio - 1
            if ratio < 1:
                # Insert a sample with some probability.
                if np.random.rand() < ratio:
                    y_val = self.data_buffer.pop(0)
                    t_, v_ = self.ts.push(0, y_val, dt, self.chart_width)
                    self.scaling_buffer.append(y_val)
            else:
                # Definitely insert one sample.
                y_val = self.data_buffer.pop(0)
                t_, v_ = self.ts.push(0, y_val, dt, self.chart_width)
                self.scaling_buffer.append(y_val)

                # Insert another sample with some probability.
                if np.random.rand() < excess and len(self.data_buffer) > 100:
                    y_val = self.data_buffer.pop(0)
                    t_, v_ = self.ts.push(0, y_val, dt, self.chart_width)
                    self.scaling_buffer.append(y_val)

            if len(self.data_buffer) == 0:
                # We need to re-buffer the data, for some reason.
                self.buffered = False

            try:
                # Draw updated graph on the canvas.
                self.cartesian.draw(t_, v_)
            except:
                pass

            if self.autoscale:
                self.update_scale()

    def update_scale(self):
        # Perform autoscaling based on max/min values.
        y_max = np.max(self.scaling_buffer)
        y_min = np.min(self.scaling_buffer)
        margin = 0.1 * (y_max - y_min)
        y_max *= 1 + margin
        y_min *= 1 - margin
        a = 0.01
        max_value = float((1 - a) * self.chart_max + a * y_max)
        min_value = float((1 - a) * self.chart_min + a * y_min)
        self.set_chart_max(max_value)
        self.set_chart_min(min_value)


class ChartApp(App):

    def build(self):
        chart = Chart()
        chart.init()
        chart.sensor_name = "PPG Sensor"
        chart.cartesian.init()
        Clock.schedule_interval(chart.tick, 1.0 / 100)
        return chart


if __name__ == "__main__":

    # Run the biomonitor.
    ChartApp().run()
