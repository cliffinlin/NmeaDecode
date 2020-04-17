#!/usr/bin/env python
from geopy import distance

from Statistic import Statistic
from Plot import Plot

SEPARATOR_N = "\n"
SEPARATOR_T = "\t"

FILE_NAME_EXT_STATISTIC = ".statistic"


class NmeaStatistic:
    def __init__(self):
        self.FileName = FILE_NAME_EXT_STATISTIC
        self.OutputFile = None

        self.LastNavigateData = None

        self.DistanceFromLastPoint = 0
        self.TotalDistance = 0

        self.FixQuality = None

        self.PDOPList = []
        self.HDOPList = []
        self.VDOPList = []

        self.LatitudeList = []
        self.LongitudeList = []

        self.PDOTStatistic = Statistic()
        self.HDOTStatistic = Statistic()
        self.VDOTStatistic = Statistic()
        self.LatitudeStatistic = Statistic()
        self.LongitudeStatistic = Statistic()

        self.Plot = Plot()

    def set_file_name(self, file_name):
        self.FileName = file_name + FILE_NAME_EXT_STATISTIC

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

        self.PDOPList.append(navigate_data.PDOP)
        self.HDOPList.append(navigate_data.HDOP)
        self.VDOPList.append(navigate_data.VDOP)
        self.LatitudeList.append(navigate_data.LatitudeValue)
        self.LongitudeList.append(navigate_data.LongitudeValue)

        self.LastNavigateData = navigate_data

        self.write_to_file(navigate_data)

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
                   + str(self.DistanceFromLastPoint) + SEPARATOR_T \
                   + str(self.TotalDistance) + SEPARATOR_N
            self.OutputFile.write(text)

    def statistic(self):
        self.PDOTStatistic.statistic("PDOP", self.PDOPList)
        self.HDOTStatistic.statistic("HDOP", self.HDOPList)
        self.VDOTStatistic.statistic("VDOP", self.VDOPList)
        self.LatitudeStatistic.statistic("Latitude", self.LatitudeList)
        self.LongitudeStatistic.statistic("Longitude", self.LongitudeList)

        self.Plot.draw(self.LongitudeStatistic, self.LatitudeStatistic)

        if self.OutputFile is not None:
            self.OutputFile.close()

    def to_string(self):
        result = ""

        result += self.PDOTStatistic.to_string() + SEPARATOR_N \
                  + self.HDOTStatistic.to_string() + SEPARATOR_N \
                  + self.VDOTStatistic.to_string() + SEPARATOR_N

        return result
