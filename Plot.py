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

    def draw(self, longitude_mean_variance, latitude_mean_variance):
        if longitude_mean_variance is None or latitude_mean_variance is None:
            return

        longitude_offset = max(abs(longitude_mean_variance.Mean - longitude_mean_variance.Min),
                               abs(longitude_mean_variance.Mean - longitude_mean_variance.Max))
        latitude_offset = max(abs(latitude_mean_variance.Mean - latitude_mean_variance.Min),
                              abs(latitude_mean_variance.Mean - latitude_mean_variance.Max))

        self.llcrnrlon = longitude_mean_variance.Mean - longitude_offset
        self.llcrnrlat = latitude_mean_variance.Mean - latitude_offset
        self.urcrnrlon = longitude_mean_variance.Mean + longitude_offset
        self.urcrnrlat = latitude_mean_variance.Mean + latitude_offset

        self.lon_0 = longitude_mean_variance.Mean
        self.lat_0 = latitude_mean_variance.Mean

        map = Basemap(llcrnrlon=self.llcrnrlon, llcrnrlat=self.llcrnrlat, urcrnrlon=self.urcrnrlon,
                      urcrnrlat=self.urcrnrlat, projection='lcc', suppress_ticks=False,
                      resolution='i', lat_0=self.lat_0, lon_0=self.lon_0)

        x, y = map(longitude_mean_variance.DataList, latitude_mean_variance.DataList)

        map.scatter(x, y)

        map.drawcoastlines()

        plt.show()
