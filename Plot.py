#!/usr/bin/python
from matplotlib.patches import Circle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from Statistic import Statistic

SEPARATOR_N = "\n"


class Plot:
    def __init__(self):
        self.Basemap = None

        self.llcrnrlon = None
        self.llcrnrlat = None
        self.urcrnrlon = None
        self.urcrnrlat = None
        self.lon_0 = None
        self.lat_0 = None

        self.lons = []
        self.lats = []

        self.XList = []
        self.YList = []

        self.XStatistic = Statistic()
        self.YStatistic = Statistic()

        self.CEP = 0
        self.CEP95 = 0
        self.CEP99 = 0

    def convert(self, longitude_statistic, latitude_statistic):
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

        self.Basemap = Basemap(llcrnrlon=self.llcrnrlon, llcrnrlat=self.llcrnrlat, urcrnrlon=self.urcrnrlon,
                           urcrnrlat=self.urcrnrlat, projection='lcc', suppress_ticks=False,
                           resolution='i', lat_0=self.lat_0, lon_0=self.lon_0)

        self.XList, self.YList = self.Basemap(longitude_statistic.DataList, latitude_statistic.DataList)

        self.XStatistic.statistic("X", self.XList)
        self.YStatistic.statistic("Y", self.YList)

        # 点位精度评定 https://blog.csdn.net/weixin_30670151/article/details/99243902
        self.CEP = 0.589 * (self.XStatistic.Std + self.YStatistic.Std)
        self.CEP95 = 1.2272 * (self.XStatistic.Std + self.YStatistic.Std)
        self.CEP99 = 1.5222 * (self.XStatistic.Std + self.YStatistic.Std)

        print(self.cep_to_string())

    def draw(self):
        self.Basemap.scatter(self.XList, self.YList)

        x0 = self.XStatistic.Mean
        y0 = self.YStatistic.Mean

        max_radius = 5
        x_axis = (x0 - max_radius, x0 + max_radius)
        y_axis = (y0 - max_radius, y0 + max_radius)

        plt.plot(x_axis, (y0, y0), color='grey')
        plt.plot((x0, x0), y_axis, color='grey')

        # text = str(self.lat_0) + ", " + str(self.lon_0) + ", "\
        #        + "CEP=" + str(self.CEP) + ", "\
        #        + "CEP95=" + str(self.CEP95) + ", " \
        #        + "CEP99=" + str(self.CEP99)
        # plt.text(x0, y0, text)

        for i in range(0, max_radius):
            circle = Circle((x0, y0), radius=i + 1, fill=False, color='#00ffff', alpha=0.5)
            plt.gca().add_patch(circle)

        circle = Circle((x0, y0), radius=self.CEP, fill=False, color='red')
        plt.gca().add_patch(circle)

        circle = Circle((x0, y0), radius=self.CEP95, fill=False, color='red')
        plt.gca().add_patch(circle)

        circle = Circle((x0, y0), radius=self.CEP99, fill=False, color='red')
        plt.gca().add_patch(circle)

        plt.show()

    def cep_to_string(self):
        result = ""

        result += "CEP = " + str(self.CEP) + SEPARATOR_N \
                  + "CEP95 = " + str(self.CEP95) + SEPARATOR_N \
                  + "CEP99 = " + str(self.CEP99) + SEPARATOR_N

        return result

    def to_string(self):
        result = ""

        result += self.XStatistic.to_string() + SEPARATOR_N \
                  + self.YStatistic.to_string() + SEPARATOR_N \
                  + self.cep_to_string() + SEPARATOR_N

        return result
