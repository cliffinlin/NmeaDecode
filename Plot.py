#!/usr/bin/python
from matplotlib.patches import Circle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


class Plot:
    def __init__(self):
        self.llcrnrlon = None
        self.llcrnrlat = None
        self.urcrnrlon = None
        self.urcrnrlat = None
        self.lon_0 = None
        self.lat_0 = None

        self.lons = []
        self.lats = []

    def draw(self, longitude_statistic, latitude_statistic):
        if not longitude_statistic.valid():
            return

        if not latitude_statistic.valid():
            return

        a = 1
        b = 0.001
        longitude_offset = a * max(abs(longitude_statistic.Mean - longitude_statistic.Min),
                               abs(longitude_statistic.Mean - longitude_statistic.Max)) + b
        latitude_offset = a * max(abs(latitude_statistic.Mean - latitude_statistic.Min),
                              abs(latitude_statistic.Mean - latitude_statistic.Max)) + b

        self.llcrnrlon = longitude_statistic.Mean - longitude_offset
        self.llcrnrlat = latitude_statistic.Mean - latitude_offset
        self.urcrnrlon = longitude_statistic.Mean + longitude_offset
        self.urcrnrlat = latitude_statistic.Mean + latitude_offset

        self.lon_0 = longitude_statistic.Mean
        self.lat_0 = latitude_statistic.Mean

        map = Basemap(llcrnrlon=self.llcrnrlon, llcrnrlat=self.llcrnrlat, urcrnrlon=self.urcrnrlon,
                      urcrnrlat=self.urcrnrlat, projection='lcc', suppress_ticks=False,
                      resolution='i', lat_0=self.lat_0, lon_0=self.lon_0)

        x, y = map(longitude_statistic.DataList, latitude_statistic.DataList)
        x0, y0 = map(longitude_statistic.Mean, latitude_statistic.Mean)

        map.scatter(x, y)

        maxRadius = 5
        x_axix = (x0 - maxRadius, x0 + maxRadius)
        y_axix = (y0 - maxRadius, y0 + maxRadius)

        plt.plot(x_axix, (y0, y0), color='red')
        plt.plot((x0, x0), y_axix, color='red')

        text = str(self.lat_0) + ", " + str(self.lon_0)
        plt.text(x0, y0, text)

        for i in range(0, maxRadius):
            circle = Circle((x0, y0), radius=i+1, fill=False, color='r')
            plt.gca().add_patch(circle)

        plt.show()
