#!/usr/bin/python

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

    def set_domain(self, llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat):
        self.llcrnrlon = llcrnrlon
        self.llcrnrlat = llcrnrlat
        self.urcrnrlon = urcrnrlon
        self.urcrnrlat = urcrnrlat

        self.lon_0 = (self.llcrnrlon + self.urcrnrlon) / 2.0
        self.lat_0 = (self.llcrnrlat + self.urcrnrlat) / 2.0

    def draw(self, lons, lats):
        map = Basemap(llcrnrlon=self.llcrnrlon, llcrnrlat=self.llcrnrlat, urcrnrlon=self.urcrnrlon,
                      urcrnrlat=self.urcrnrlat, projection='lcc', suppress_ticks=False,
                      resolution='i', lat_0=self.lat_0, lon_0=self.lon_0)

        x, y = map(lons, lats)

        map.scatter(x, y)

        map.drawcoastlines()

        plt.show()
