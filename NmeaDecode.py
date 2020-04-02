#!/usr/bin/env python

import os
import sys

import folium

from BDGGA import BDGGA
from BDGLL import BDGLL
from BDGSA import BDGSA
from BDGSV import BDGSV
from BDRMC import BDRMC
from BDVTG import BDVTG
from FoliumMap import FoliumMap
from GNGGA import GNGGA
from GNGLL import GNGLL
from GNGSA import GNGSA
from GNGSV import GNGSV
from GNRMC import GNRMC
from GNVTG import GNVTG
from GPGGA import GPGGA
from GPGLL import GPGLL
from GPGSA import GPGSA
from GPGSV import GPGSV
from GPRMC import GPRMC
from GPVTG import GPVTG
from NavigateData import NavigateData
from LogFile import LogFile

FILE_NAME_EXT_OUTPUT = ".out"


class NmeaDecode:
    def __init__(self):
        self.GPRMC = GPRMC()
        self.BDRMC = BDRMC()
        self.GNRMC = GNRMC()

        self.GPVTG = GPVTG()
        self.BDVTG = BDVTG()
        self.GNVTG = GNVTG()

        self.GPGGA = GPGGA()
        self.BDGGA = BDGGA()
        self.GNGGA = GNGGA()

        self.GPGSA = GPGSA()
        self.BDGSA = BDGSA()
        self.GNGSA = GNGSA()

        self.GPGSV = GPGSV()
        self.BDGSV = BDGSV()
        self.GNGSV = GNGSV()

        self.GPGLL = GPGLL()
        self.BDGLL = BDGLL()
        self.GNGLL = GNGLL()

        self.NavigateDataList = []

        self.LastSentence = ""
        self.Sentence = ""

        self.LogFileName = None
        self.LogFileNameSorted = None
        self.FileNameOut = None

        self.InputFile = None
        self.OutputFile = None

    def set_file_name(self, log_file_name, log_file_name_sorted):
        self.LogFileName = log_file_name
        self.LogFileNameSorted = log_file_name_sorted

        self.FileNameOut = self.LogFileName + FILE_NAME_EXT_OUTPUT

    def decode(self):
        if not os.path.exists(self.LogFileNameSorted):
            print(self.LogFileNameSorted, "file not found!")
            sys.exit()

        self.OutputFile = open(self.FileNameOut, "w")

        with open(self.LogFileNameSorted) as self.InputFile:
            navigate_data = NavigateData()

            for line in self.InputFile:
                if line is None:
                    continue

                if len(self.LastSentence) > 0 and self.LastSentence in line:
                    continue

                if "$GPRMC" in line:
                    self.GPRMC.decode(line)
                    self.set_last_sentence(self.GPRMC.Sentence)
                    self.write_to_file(self.GPRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.GPRMC.Date, self.GPRMC.Day, self.GPRMC.Month, self.GPRMC.Year)

                if "$BDRMC" in line:
                    self.BDRMC.decode(line)
                    self.set_last_sentence(self.BDRMC.Sentence)
                    self.write_to_file(self.BDRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.BDRMC.Date, self.BDRMC.Day, self.BDRMC.Month, self.BDRMC.Year)

                if "$GNRMC" in line:
                    self.GNRMC.decode(line)
                    self.set_last_sentence(self.GNRMC.Sentence)
                    self.write_to_file(self.GNRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.GNRMC.Date, self.GNRMC.Day, self.GNRMC.Month, self.GNRMC.Year)

                elif "$GPVTG" in line:
                    self.GPVTG.decode(line)
                    self.set_last_sentence(self.GPVTG.Sentence)
                    self.write_to_file(self.GPVTG.to_string())

                    navigate_data.set_speed_n(self.GPVTG.SpeedN)
                    navigate_data.set_speed_m(self.GPVTG.SpeedM)

                elif "$BDVTG" in line:
                    self.BDVTG.decode(line)
                    self.set_last_sentence(self.BDVTG.Sentence)
                    self.write_to_file(self.BDVTG.to_string())

                    navigate_data.set_speed_n(self.BDVTG.SpeedN)
                    navigate_data.set_speed_m(self.BDVTG.SpeedM)

                elif "$GNVTG" in line:
                    self.GNVTG.decode(line)
                    self.set_last_sentence(self.GNVTG.Sentence)
                    self.write_to_file(self.GNVTG.to_string())

                    navigate_data.set_speed_n(self.GNVTG.SpeedN)
                    navigate_data.set_speed_m(self.GNVTG.SpeedM)

                elif "$GPGGA" in line:
                    self.GPGGA.decode(line)
                    self.set_last_sentence(self.GPGGA.Sentence)
                    self.write_to_file(self.GPGGA.to_string())

                    navigate_data.set_time(self.GPGGA.Time, self.GPGGA.Hour, self.GPGGA.Minute, self.GPGGA.Second)
                    navigate_data.set_latitude(self.GPGGA.Latitude, self.GPGGA.LatitudeValue)
                    navigate_data.set_longitude(self.GPGGA.Longitude, self.GPGGA.LongitudeValue)
                    navigate_data.set_altitude(self.GPGGA.Altitude)
                    navigate_data.set_fix_quality(self.GPGGA.FixQuality)
                    navigate_data.set_tracked_number(self.GPGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.GPGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.GPGGA.ReferenceStationID)

                elif "$BDGGA" in line:
                    self.BDGGA.decode(line)
                    self.set_last_sentence(self.BDGGA.Sentence)
                    self.write_to_file(self.BDGGA.to_string())

                    navigate_data.set_time(self.BDGGA.Time, self.BDGGA.Hour, self.BDGGA.Minute, self.BDGGA.Second)
                    navigate_data.set_latitude(self.BDGGA.Latitude, self.BDGGA.LatitudeValue)
                    navigate_data.set_longitude(self.BDGGA.Longitude, self.BDGGA.LongitudeValue)
                    navigate_data.set_altitude(self.BDGGA.Altitude)
                    navigate_data.set_fix_quality(self.BDGGA.FixQuality)
                    navigate_data.set_tracked_number(self.BDGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.BDGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.BDGGA.ReferenceStationID)

                elif "$GNGGA" in line:
                    self.GNGGA.decode(line)
                    self.set_last_sentence(self.GNGGA.Sentence)
                    self.write_to_file(self.GNGGA.to_string())

                    navigate_data.set_time(self.GNGGA.Time, self.GNGGA.Hour, self.GNGGA.Minute, self.GNGGA.Second)
                    navigate_data.set_latitude(self.GNGGA.Latitude, self.GNGGA.LatitudeValue)
                    navigate_data.set_longitude(self.GNGGA.Longitude, self.GNGGA.LongitudeValue)
                    navigate_data.set_altitude(self.GNGGA.Altitude)
                    navigate_data.set_fix_quality(self.GNGGA.FixQuality)
                    navigate_data.set_tracked_number(self.GNGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.GNGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.GNGGA.ReferenceStationID)

                elif "$GPGSA" in line:
                    self.GPGSA.decode(line)
                    self.set_last_sentence(self.GPGSA.Sentence)
                    self.write_to_file(self.GPGSA.to_string())

                    navigate_data.set_fix_type(self.GPGSA.FixType)
                    navigate_data.set_gps_used(self.GPGSA.Used)
                    navigate_data.set_pdop(self.GPGSA.PDOP)
                    navigate_data.set_hdop(self.GPGSA.HDOP)
                    navigate_data.set_vdop(self.GPGSA.VDOP)

                elif "$BDGSA" in line:
                    self.BDGSA.decode(line)
                    self.set_last_sentence(self.BDGSA.Sentence)
                    self.write_to_file(self.BDGSA.to_string())

                    navigate_data.set_fix_type(self.BDGSA.FixType)
                    navigate_data.set_bds_used(self.BDGSA.Used)
                    navigate_data.set_pdop(self.BDGSA.PDOP)
                    navigate_data.set_hdop(self.BDGSA.HDOP)
                    navigate_data.set_vdop(self.BDGSA.VDOP)

                elif "$GNGSA" in line:
                    self.GNGSA.decode(line)
                    self.set_last_sentence(self.GNGSA.Sentence)
                    self.write_to_file(self.GNGSA.to_string())

                    navigate_data.set_fix_type(self.GNGSA.FixType)
                    navigate_data.set_used(self.GNGSA.Used)
                    navigate_data.set_pdop(self.GNGSA.PDOP)
                    navigate_data.set_hdop(self.GNGSA.HDOP)
                    navigate_data.set_vdop(self.GNGSA.VDOP)

                elif "$GPGSV" in line:
                    self.GPGSV.decode(line)
                    self.set_last_sentence(self.GPGSV.Sentence)
                    self.write_to_file(self.GPGSV.to_string())

                    navigate_data.set_gps_view(self.GPGSV.View)
                    navigate_data.set_gps_satellite_list(self.GPGSV.SatelliteList)

                elif "$BDGSV" in line:
                    self.BDGSV.decode(line)
                    self.set_last_sentence(self.BDGSV.Sentence)
                    self.write_to_file(self.BDGSV.to_string())

                    navigate_data.set_bds_view(self.BDGSV.View)
                    navigate_data.set_bds_satellite_list(self.BDGSV.SatelliteList)

                elif "$GNGSV" in line:
                    self.GNGSV.decode(line)
                    self.set_last_sentence(self.GNGSV.Sentence)
                    self.write_to_file(self.GNGSV.to_string())

                    navigate_data.set_view(self.GNGSV.View)
                    navigate_data.set_satellite_list(self.GNGSV.SatelliteList)

                elif "$GPGLL" in line:
                    self.GPGLL.decode(line)
                    self.set_last_sentence(self.GPGLL.Sentence)
                    self.write_to_file(self.GPGLL.to_string())

                elif "$BDGLL" in line:
                    self.BDGLL.decode(line)
                    self.set_last_sentence(self.BDGLL.Sentence)
                    self.write_to_file(self.BDGLL.to_string())

                elif "$GNGLL" in line:
                    self.GNGLL.decode(line)
                    self.set_last_sentence(self.GNGLL.Sentence)
                    self.write_to_file(self.GNGLL.to_string())

                self.add_to_navigate_data_list(navigate_data)

        self.OutputFile.close()

    def set_last_sentence(self, sentence):
        if len(sentence) == 0:
            return

        self.LastSentence = sentence

    def write_to_file(self, text):
        if self.OutputFile is None:
            return

        if len(text) == 0:
            return

        self.OutputFile.write(text + "\n")

    def add_to_navigate_data_list(self, navigate_data):
        if navigate_data is None:
            return

        if navigate_data.LatitudeValue is None or navigate_data.LongitudeValue is None:
            return
        else:
            self.NavigateDataList.append(navigate_data)


def main():
    log_file = LogFile()
    log_file.sort()

    nmea_decode = NmeaDecode()
    nmea_decode.set_file_name(log_file.FileName, log_file.FileNameSorted)
    nmea_decode.decode()

    folium_map = FoliumMap()
    folium_map.set_file_name(log_file.FileName)
    folium_map.set_navigate_data_list(nmea_decode.NavigateDataList)
    folium_map.draw()

    return 0


if __name__ == "__main__":
    main()
