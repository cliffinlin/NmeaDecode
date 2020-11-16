#!/usr/bin/env python
from geopy import distance
from matplotlib.patches import Circle
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt

from Statistic import Statistic

SEPARATOR_N = "\n"
SEPARATOR_T = "\t"

FILE_NAME_EXT_DATA = ".data"
MAX_RADIUS = 10

class NmeaStatistic:
    def __init__(self):
        self.FileName = FILE_NAME_EXT_DATA
        self.OutputFile = None

        self.LastNavigateData = None

        self.DistanceFromLastPoint = 0
        self.TotalDistance = 0

        self.FixQuality_0 = 0;
        self.FixQuality_1 = 0;
        self.FixQuality_2 = 0;
        self.FixQuality_3 = 0;
        self.FixQuality_4 = 0;
        self.FixQuality_5 = 0;
        self.FixQuality_6 = 0;

        self.MarkColor = None

        self.PDOPList = []
        self.HDOPList = []
        self.VDOPList = []

        self.LatitudeList = []
        self.LongitudeList = []
        self.AltitudeList = []

        self.XList = []
        self.YList = []

        self.ColorList = []

        self.PDOTStatistic = Statistic()
        self.HDOTStatistic = Statistic()
        self.VDOTStatistic = Statistic()

        self.LatitudeStatistic = Statistic()
        self.LongitudeStatistic = Statistic()
        self.AltitudeStatistic = Statistic()

        self.XStatistic = Statistic()
        self.YStatistic = Statistic()

        self.Basemap = None

        self.CEP = 0
        self.CEP95 = 0
        self.CEP99 = 0

    def set_file_name(self, file_name):
        self.FileName = file_name + FILE_NAME_EXT_DATA

    def check_date_time(self, navigate_data):
        result = False

        if navigate_data is None:
            return result

        if navigate_data.LocalDateTime is None:
            return result

        if self.LastNavigateData is not None:
            last_local_date_time = self.LastNavigateData.LocalDateTime
            if last_local_date_time is not None:
                duration = navigate_data.LocalDateTime - last_local_date_time
                if duration.seconds <= 0:
                    return result

        result = True

        return result

    def add_to_data_list(self, navigate_data):
        self.DistanceFromLastPoint = 0

        if navigate_data is None:
            return

        if not self.check_date_time(navigate_data):
            return

        if len(navigate_data.PDOP) == 0 or len(navigate_data.HDOP) == 0 or len(navigate_data.VDOP) == 0:
            return

        if navigate_data.LatitudeValue == 0 or navigate_data.LongitudeValue == 0:
            return

        if self.LastNavigateData is not None:
            last_point = (self.LastNavigateData.LatitudeValue, self.LastNavigateData.LongitudeValue)
            current_point = (navigate_data.LatitudeValue, navigate_data.LongitudeValue)
            self.DistanceFromLastPoint = distance.distance(last_point, current_point).m

        self.TotalDistance += self.DistanceFromLastPoint

        try:
            self.PDOPList.append(navigate_data.PDOP)
            self.HDOPList.append(navigate_data.HDOP)
            self.VDOPList.append(navigate_data.VDOP)
            self.LatitudeList.append(navigate_data.LatitudeValue)
            self.LongitudeList.append(navigate_data.LongitudeValue)
            self.AltitudeList.append(float(navigate_data.Altitude))
        except ValueError as e:
            print("ValueError:", e)
            return

        # (55, 168, 218), (187, 249, 112), (255, 255, 0), (113, 130, 36), (113, 174, 38), (255, 255, 255)
        value = int(navigate_data.FixQuality)
        if value == 0:
            self.FixQuality_0 = self.FixQuality_0 + 1;
            self.MarkColor = (0.5, 0.5, 0.5)  # remark = "Invalid"
        elif value == 1:
            self.FixQuality_1 = self.FixQuality_1 + 1;
            self.MarkColor = (0.22, 0.67, 0.872)  # remark = "SPS"
        elif value == 2:
            self.FixQuality_2 = self.FixQuality_2 + 1;
            self.MarkColor = (0.733, 0.976, 0.439)  # remark = "Differential"
        elif value == 3:
            self.FixQuality_3 = self.FixQuality_3 + 1;
            self.MarkColor = (1.0, 1.0, 0)  # remark = "PPS"
        elif value == 4:
            self.FixQuality_4 = self.FixQuality_4 + 1;
            self.MarkColor = (0.443, 0.509, 0.141)  # remark = "RTK Fixed"
        elif value == 5:
            self.FixQuality_5 = self.FixQuality_5 + 1;
            self.MarkColor = (0.443, 0.682, 0.149)  # remark = "RTK Float"
        elif value == 6:
            self.FixQuality_6 = self.FixQuality_6 + 1;
            self.MarkColor = (1.0, 1.0, 1.0)  # remark = "Estimated"

        self.ColorList.append(self.MarkColor)

        self.LastNavigateData = navigate_data

        self.write_to_file(navigate_data)

    def convert(self):
        if not self.LongitudeStatistic.valid():
            return

        if not self.LatitudeStatistic.valid():
            return

        a = 1
        b = 0.001
        longitude_offset = a * max(abs(self.LongitudeStatistic.Mean - self.LongitudeStatistic.Min),
                                   abs(self.LongitudeStatistic.Mean - self.LongitudeStatistic.Max)) + b
        latitude_offset = a * max(abs(self.LatitudeStatistic.Mean - self.LatitudeStatistic.Min),
                                  abs(self.LatitudeStatistic.Mean - self.LatitudeStatistic.Max)) + b

        self.Basemap = Basemap(llcrnrlon=self.LongitudeStatistic.Mean - longitude_offset,
                               llcrnrlat=self.LatitudeStatistic.Mean - latitude_offset,
                               urcrnrlon=self.LongitudeStatistic.Mean + longitude_offset,
                               urcrnrlat=self.LatitudeStatistic.Mean + latitude_offset,
                               projection='lcc', suppress_ticks=False, resolution='i',
                               lat_0=self.LatitudeStatistic.Mean,
                               lon_0=self.LongitudeStatistic.Mean)

        self.XList, self.YList = self.Basemap(self.LongitudeStatistic.DataList, self.LatitudeStatistic.DataList)

    def write_to_file(self, navigate_data):
        if self.OutputFile is None:
            self.OutputFile = open(self.FileName, "w")
            text = "date_time" + SEPARATOR_T \
                   + "FixQuality" + SEPARATOR_T \
                   + "PDOP" + SEPARATOR_T \
                   + "HDOP" + SEPARATOR_T \
                   + "VDOP" + SEPARATOR_T \
                   + "Latitude" + SEPARATOR_T \
                   + "Longitude" + SEPARATOR_T \
                   + "Altitude" + SEPARATOR_T \
                   + "delt" + SEPARATOR_T \
                   + "total" + SEPARATOR_N
            self.OutputFile.write(text)

        if self.OutputFile is not None:
            text = navigate_data.local_date_time_to_string() + SEPARATOR_T \
                   + navigate_data.FixQuality + SEPARATOR_T \
                   + navigate_data.PDOP + SEPARATOR_T \
                   + navigate_data.HDOP + SEPARATOR_T \
                   + navigate_data.VDOP + SEPARATOR_T \
                   + str(navigate_data.LatitudeValue) + SEPARATOR_T \
                   + str(navigate_data.LongitudeValue) + SEPARATOR_T \
                   + str(navigate_data.Altitude) + SEPARATOR_T \
                   + str(self.DistanceFromLastPoint) + SEPARATOR_T \
                   + str(self.TotalDistance) + SEPARATOR_N
            self.OutputFile.write(text)

    def statistic(self):
        self.PDOTStatistic.statistic("PDOP", self.PDOPList)
        self.HDOTStatistic.statistic("HDOP", self.HDOPList)
        self.VDOTStatistic.statistic("VDOP", self.VDOPList)
        self.LatitudeStatistic.statistic("Latitude", self.LatitudeList)
        self.LongitudeStatistic.statistic("Longitude", self.LongitudeList)
        self.AltitudeStatistic.statistic("Altitude", self.AltitudeList)

        self.convert()

        self.XStatistic.statistic("X", self.XList)
        self.YStatistic.statistic("Y", self.YList)

        self.CEP = Statistic.cep(self.XStatistic.Std, self.YStatistic.Std)
        self.CEP95 = Statistic.cep95(self.XStatistic.Std, self.YStatistic.Std)
        self.CEP99 = Statistic.cep99(self.XStatistic.Std, self.YStatistic.Std)

        print(self.cep_to_string())
        print(self.rms_to_string())
        print(self.test_point_count_to_string())
        print(self.fix_quality_count_to_string())

        if self.OutputFile is not None:
            self.OutputFile.write(self.to_string())
            self.OutputFile.close()

    def draw(self):
        if self.Basemap is None:
            return

        self.Basemap.scatter(self.XList, self.YList, c=self.ColorList)

        x0 = self.XStatistic.Mean
        y0 = self.YStatistic.Mean

        # MAX_RADIUS = 10
        x_axis = (x0 - MAX_RADIUS, x0 + MAX_RADIUS)
        y_axis = (y0 - MAX_RADIUS, y0 + MAX_RADIUS)

        plt.plot(x_axis, (y0, y0), color='grey')
        plt.plot((x0, x0), y_axis, color='grey')

        for i in range(0, MAX_RADIUS):
            circle = Circle((x0, y0), radius=i + 1, fill=False, color='#00ffff', alpha=0.5)
            plt.gca().add_patch(circle)
            plt.text(x0 + i + 1, y0, i + 1)

        circle = Circle((x0, y0), radius=self.CEP, fill=False, color='red')
        plt.gca().add_patch(circle)
        plt.text(x0, y0 + self.CEP, ("%.4f" % self.CEP))

        circle = Circle((x0, y0), radius=self.CEP95, fill=False, color='red')
        plt.gca().add_patch(circle)
        plt.text(x0, y0 + self.CEP95, ("%.4f" % self.CEP95))

        circle = Circle((x0, y0), radius=self.CEP99, fill=False, color='red')
        plt.gca().add_patch(circle)
        plt.text(x0, y0 + self.CEP99, ("%.4f" % self.CEP99))

        plt.show()

    def test_point_count_to_string(self):
        result = ""

        result += "Test point count = " + str(len(self.XList)) + SEPARATOR_N

        return result

    def fix_quality_count_to_string(self):
        result = ""

        if self.FixQuality_0 > 0:
            result += "Invalid count = " + str(self.FixQuality_0) + SEPARATOR_N

        if self.FixQuality_1 > 0:
            result += "SPS count = " + str(self.FixQuality_1) + SEPARATOR_N

        if self.FixQuality_2 > 0:
            result += "Differential count = " + str(self.FixQuality_2) + SEPARATOR_N

        if self.FixQuality_3 > 0:
            result += "PPS count = " + str(self.FixQuality_3) + SEPARATOR_N

        if self.FixQuality_4 > 0:
            result += "RTK Fixed count = " + str(self.FixQuality_4) + SEPARATOR_N

        if self.FixQuality_5 > 0:
            result += "RTK Float count = " + str(self.FixQuality_5) + SEPARATOR_N

        if self.FixQuality_6 > 0:
            result += "Estimated count = " + str(self.FixQuality_6) + SEPARATOR_N

        return result

    def rms_to_string(self):
        result = ""

        result += "RMS_H = " + str(1.2 * self.CEP) + SEPARATOR_N \
                  + "RMS_V = " + str(self.AltitudeStatistic.Std) + SEPARATOR_N

        return result

    def cep_to_string(self):
        result = ""

        result += "CEP = " + str(self.CEP) + SEPARATOR_N \
                  + "CEP95 = " + str(self.CEP95) + SEPARATOR_N \
                  + "CEP99 = " + str(self.CEP99) + SEPARATOR_N

        return result

    def to_string(self):
        result = ""

        result += self.PDOTStatistic.to_string() + SEPARATOR_N \
                  + self.HDOTStatistic.to_string() + SEPARATOR_N \
                  + self.VDOTStatistic.to_string() + SEPARATOR_N \
                  + self.LatitudeStatistic.to_string() + SEPARATOR_N \
                  + self.LongitudeStatistic.to_string() + SEPARATOR_N \
                  + self.AltitudeStatistic.to_string() + SEPARATOR_N \
                  + self.XStatistic.to_string() + SEPARATOR_N \
                  + self.YStatistic.to_string() + SEPARATOR_N \
                  + self.cep_to_string() + SEPARATOR_N \
                  + self.rms_to_string() + SEPARATOR_N \
                  + self.test_point_count_to_string() + SEPARATOR_N\
                  + self.fix_quality_count_to_string()

        return result
