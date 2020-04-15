#!/usr/bin/env python
from MeanVariance import MeanVariance

SEPARATE_STRING = "\n"
FILE_NAME_EXT_DOP = ".dop"


class Statistic:
    def __init__(self):
        self.Separate = SEPARATE_STRING

        self.FileName = FILE_NAME_EXT_DOP
        self.OutputFile = None

        self.LastDateTime = None

        self.PDOPList = []
        self.HDOPList = []
        self.VDOPList = []

        self.PDOTMeanVariance = MeanVariance()
        self.HDOTMeanVariance = MeanVariance()
        self.VDOTMeanVariance = MeanVariance()

    def set_file_name(self, file_name):
        self.FileName = file_name + FILE_NAME_EXT_DOP

    def add_to_dop_data_list(self, navigate_data):
        if navigate_data is None:
            return

        if navigate_data.LocalDateTime is None:
            return

        if len(navigate_data.PDOP) == 0 or len(navigate_data.HDOP) == 0 or len(navigate_data.VDOP) == 0:
            return

        if self.LastDateTime is not None:
            duration = navigate_data.LocalDateTime - self.LastDateTime
            if duration.seconds <= 0:
                return

        self.LastDateTime = navigate_data.LocalDateTime

        self.PDOPList.append(navigate_data.PDOP)
        self.HDOPList.append(navigate_data.HDOP)
        self.VDOPList.append(navigate_data.VDOP)

        if self.OutputFile is None:
            self.OutputFile = open(self.FileName, "w")

        if self.OutputFile is not None:
            text = navigate_data.local_date_time_to_string() + "\t" + navigate_data.PDOP + "\t" + navigate_data.HDOP + "\t" + navigate_data.VDOP + "\n"
            print(text)
            self.OutputFile.write(text)

    def statistic(self):
        self.PDOTMeanVariance.statistic("PDOP", self.PDOPList)
        self.HDOTMeanVariance.statistic("HDOP", self.HDOPList)
        self.VDOTMeanVariance.statistic("VDOP", self.VDOPList)

        if self.OutputFile is not None:
            self.OutputFile.close()

    def to_string(self):
        result = ""

        result += self.PDOTMeanVariance.to_string() + self.Separate \
                  + self.HDOTMeanVariance.to_string() + self.Separate \
                  + self.VDOTMeanVariance.to_string() + self.Separate

        return result
