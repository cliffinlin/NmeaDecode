#!/usr/bin/env python
import datetime
import os
import sys

from BDGGA import BDGGA
from BDGLL import BDGLL
from BDGSA import BDGSA
from BDGSV import BDGSV
from BDRMC import BDRMC
from BDVTG import BDVTG
from GBGGA import GBGGA
from GBGLL import GBGLL
from GBGSA import GBGSA
from GLGSV import GLGSV
from GBGSV import GBGSV
from GBRMC import GBRMC
from GBVTG import GBVTG
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
from NmeaStatistic import NmeaStatistic

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_TIME_FROM = None
DATE_TIME_TO = None

# DATE_TIME_FROM = "2020-09-10 08:36:00"
# DATE_TIME_TO = "2020-09-10 08:46:00"

FILE_NAME_EXT_OUT = ".out"

class NmeaDecode:
    def __init__(self):
        self.GPRMC = GPRMC()
        self.BDRMC = BDRMC()
        self.GBRMC = GBRMC()
        self.GNRMC = GNRMC()

        self.GPVTG = GPVTG()
        self.BDVTG = BDVTG()
        self.GBVTG = GBVTG()
        self.GNVTG = GNVTG()

        self.GPGGA = GPGGA()
        self.BDGGA = BDGGA()
        self.GBGGA = GBGGA()
        self.GNGGA = GNGGA()

        self.GPGSA = GPGSA()
        self.BDGSA = BDGSA()
        self.GBGSA = GBGSA()
        self.GNGSA = GNGSA()

        self.GPGSV = GPGSV()
        self.GLGSV = GLGSV()
        self.BDGSV = BDGSV()
        self.GBGSV = GBGSV()
        self.GNGSV = GNGSV()

        self.GPGLL = GPGLL()
        self.BDGLL = BDGLL()
        self.GBGLL = GBGLL()
        self.GNGLL = GNGLL()

        self.DateTimeFrom = None
        self.DateTimeTo = None

        self.LastSentence = ""
        self.Sentence = ""

        self.LogFileName = None
        self.LogFileNameSorted = None

        self.InputFile = None

        self.NmeaFile = None
        self.NmeaFileName = None

        self.OutputFile = None
        self.OutputFileName = None

        self.NavigateDataList = []

        self.NmeaStatistic = NmeaStatistic()

        self.setup_date_time_from()
        self.setup_date_time_to()

    def set_file_name(self, log_file_name, log_file_name_sorted):
        self.LogFileName = log_file_name
        self.LogFileNameSorted = log_file_name_sorted

        self.NmeaFileName = self.LogFileName + FILE_NAME_EXT_NMEA
        self.OutputFileName = self.LogFileName + FILE_NAME_EXT_OUT
        self.NmeaStatistic.set_file_name(self.LogFileName)

    def decode(self):
        if not os.path.exists(self.LogFileNameSorted):
            print(self.LogFileNameSorted, "file not found!")
            sys.exit()

        self.NmeaFile = open(self.NmeaFileName, "w")
        self.OutputFile = open(self.OutputFileName, "w")

        with open(self.LogFileNameSorted) as self.InputFile:
            navigate_data = NavigateData()

            for line in self.InputFile:
                if line is None:
                    continue

                if len(self.LastSentence) > 0 and self.LastSentence in line:
                    continue

                if "$GPRMC" in line:
                    if not self.GPRMC.decode(line):
                        continue

                    self.set_last_sentence(self.GPRMC.Sentence)
                    self.write_to_output_file(self.GPRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.GPRMC.Date, self.GPRMC.Day, self.GPRMC.Month, self.GPRMC.Year)

                if "$BDRMC" in line:
                    if not self.BDRMC.decode(line):
                        continue

                    self.set_last_sentence(self.BDRMC.Sentence)
                    self.write_to_output_file(self.BDRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.BDRMC.Date, self.BDRMC.Day, self.BDRMC.Month, self.BDRMC.Year)

                if "$GBRMC" in line:
                    if not self.GBRMC.decode(line):
                        continue

                    self.set_last_sentence(self.GBRMC.Sentence)
                    self.write_to_output_file(self.GBRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.GBRMC.Date, self.GBRMC.Day, self.GBRMC.Month, self.GBRMC.Year)

                if "$GNRMC" in line:
                    if not self.GNRMC.decode(line):
                        continue

                    self.set_last_sentence(self.GNRMC.Sentence)
                    self.write_to_output_file(self.GNRMC.to_string())

                    navigate_data = NavigateData()

                    navigate_data.set_date(self.GNRMC.Date, self.GNRMC.Day, self.GNRMC.Month, self.GNRMC.Year)

                elif "$GPVTG" in line:
                    if not self.GPVTG.decode(line):
                        continue

                    self.set_last_sentence(self.GPVTG.Sentence)
                    self.write_to_output_file(self.GPVTG.to_string())

                    navigate_data.set_speed_n(self.GPVTG.SpeedN)
                    navigate_data.set_speed_m(self.GPVTG.SpeedM)

                elif "$BDVTG" in line:
                    if not self.BDVTG.decode(line):
                        continue

                    self.set_last_sentence(self.BDVTG.Sentence)
                    self.write_to_output_file(self.BDVTG.to_string())

                    navigate_data.set_speed_n(self.BDVTG.SpeedN)
                    navigate_data.set_speed_m(self.BDVTG.SpeedM)

                elif "$GBVTG" in line:
                    if not self.GBVTG.decode(line):
                        continue

                    self.set_last_sentence(self.GBVTG.Sentence)
                    self.write_to_output_file(self.GBVTG.to_string())

                    navigate_data.set_speed_n(self.GBVTG.SpeedN)
                    navigate_data.set_speed_m(self.GBVTG.SpeedM)

                elif "$GNVTG" in line:
                    if not self.GNVTG.decode(line):
                        continue

                    self.set_last_sentence(self.GNVTG.Sentence)
                    self.write_to_output_file(self.GNVTG.to_string())

                    navigate_data.set_speed_n(self.GNVTG.SpeedN)
                    navigate_data.set_speed_m(self.GNVTG.SpeedM)

                elif "$GPGGA" in line:
                    if not self.GPGGA.decode(line):
                        continue

                    self.set_last_sentence(self.GPGGA.Sentence)
                    self.write_to_output_file(self.GPGGA.to_string())

                    navigate_data.set_time(self.GPGGA.Time, self.GPGGA.Hour, self.GPGGA.Minute, self.GPGGA.Second)
                    navigate_data.set_latitude(self.GPGGA.Latitude, self.GPGGA.LatitudeValue)
                    navigate_data.set_longitude(self.GPGGA.Longitude, self.GPGGA.LongitudeValue)
                    navigate_data.set_altitude(self.GPGGA.Altitude)
                    navigate_data.set_fix_quality(self.GPGGA.FixQuality)
                    navigate_data.set_tracked_number(self.GPGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.GPGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.GPGGA.ReferenceStationID)

                elif "$BDGGA" in line:
                    if not self.BDGGA.decode(line):
                        continue

                    self.set_last_sentence(self.BDGGA.Sentence)
                    self.write_to_output_file(self.BDGGA.to_string())

                    navigate_data.set_time(self.BDGGA.Time, self.BDGGA.Hour, self.BDGGA.Minute, self.BDGGA.Second)
                    navigate_data.set_latitude(self.BDGGA.Latitude, self.BDGGA.LatitudeValue)
                    navigate_data.set_longitude(self.BDGGA.Longitude, self.BDGGA.LongitudeValue)
                    navigate_data.set_altitude(self.BDGGA.Altitude)
                    navigate_data.set_fix_quality(self.BDGGA.FixQuality)
                    navigate_data.set_tracked_number(self.BDGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.BDGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.BDGGA.ReferenceStationID)

                elif "$GBGGA" in line:
                    if not self.GBGGA.decode(line):
                        continue

                    self.set_last_sentence(self.GBGGA.Sentence)
                    self.write_to_output_file(self.GBGGA.to_string())

                    navigate_data.set_time(self.GBGGA.Time, self.GBGGA.Hour, self.GBGGA.Minute, self.GBGGA.Second)
                    navigate_data.set_latitude(self.GBGGA.Latitude, self.GBGGA.LatitudeValue)
                    navigate_data.set_longitude(self.GBGGA.Longitude, self.GBGGA.LongitudeValue)
                    navigate_data.set_altitude(self.GBGGA.Altitude)
                    navigate_data.set_fix_quality(self.GBGGA.FixQuality)
                    navigate_data.set_tracked_number(self.GBGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.GBGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.GBGGA.ReferenceStationID)

                elif "$GNGGA" in line:
                    if not self.GNGGA.decode(line):
                        continue

                    self.set_last_sentence(self.GNGGA.Sentence)
                    self.write_to_output_file(self.GNGGA.to_string())

                    navigate_data.set_time(self.GNGGA.Time, self.GNGGA.Hour, self.GNGGA.Minute, self.GNGGA.Second)
                    navigate_data.set_latitude(self.GNGGA.Latitude, self.GNGGA.LatitudeValue)
                    navigate_data.set_longitude(self.GNGGA.Longitude, self.GNGGA.LongitudeValue)
                    navigate_data.set_altitude(self.GNGGA.Altitude)
                    navigate_data.set_fix_quality(self.GNGGA.FixQuality)
                    navigate_data.set_tracked_number(self.GNGGA.TrackedNumber)
                    navigate_data.set_differential_data_age(self.GNGGA.DifferentialDataAge)
                    navigate_data.set_reference_station_id(self.GNGGA.ReferenceStationID)

                elif "$GPGSA" in line:
                    if not self.GPGSA.decode(line):
                        continue

                    self.set_last_sentence(self.GPGSA.Sentence)
                    self.write_to_output_file(self.GPGSA.to_string())

                    navigate_data.set_fix_type(self.GPGSA.FixType)
                    navigate_data.set_gps_used(self.GPGSA.Used)
                    navigate_data.set_pdop(self.GPGSA.PDOP)
                    navigate_data.set_hdop(self.GPGSA.HDOP)
                    navigate_data.set_vdop(self.GPGSA.VDOP)

                elif "$BDGSA" in line:
                    if not self.BDGSA.decode(line):
                        continue

                    self.set_last_sentence(self.BDGSA.Sentence)
                    self.write_to_output_file(self.BDGSA.to_string())

                    navigate_data.set_fix_type(self.BDGSA.FixType)
                    navigate_data.set_bds_used(self.BDGSA.Used)
                    navigate_data.set_pdop(self.BDGSA.PDOP)
                    navigate_data.set_hdop(self.BDGSA.HDOP)
                    navigate_data.set_vdop(self.BDGSA.VDOP)

                elif "$GBGSA" in line:
                    if not self.GBGSA.decode(line):
                        continue

                    self.set_last_sentence(self.GBGSA.Sentence)
                    self.write_to_output_file(self.GBGSA.to_string())

                    navigate_data.set_fix_type(self.GBGSA.FixType)
                    navigate_data.set_bds_used(self.GBGSA.Used)
                    navigate_data.set_pdop(self.GBGSA.PDOP)
                    navigate_data.set_hdop(self.GBGSA.HDOP)
                    navigate_data.set_vdop(self.GBGSA.VDOP)

                elif "$GNGSA" in line:
                    if not self.GNGSA.decode(line):
                        continue

                    self.set_last_sentence(self.GNGSA.Sentence)
                    self.write_to_output_file(self.GNGSA.to_string())

                    navigate_data.set_fix_type(self.GNGSA.FixType)
                    navigate_data.set_used(self.GNGSA.Used)
                    navigate_data.set_pdop(self.GNGSA.PDOP)
                    navigate_data.set_hdop(self.GNGSA.HDOP)
                    navigate_data.set_vdop(self.GNGSA.VDOP)

                elif "$GPGSV" in line:
                    if not self.GPGSV.decode(line):
                        continue

                    self.set_last_sentence(self.GPGSV.Sentence)
                    self.write_to_output_file(self.GPGSV.to_string())

                    navigate_data.set_gps_view(self.GPGSV.View)
                    navigate_data.set_gps_satellite_list(self.GPGSV.SatelliteList)

                elif "$GLGSV" in line:
                    if not self.GLGSV.decode(line):
                        continue

                    self.set_last_sentence(self.GLGSV.Sentence)
                    self.write_to_output_file(self.GLGSV.to_string())

                    navigate_data.set_glo_view(self.GLGSV.View)
                    navigate_data.set_glo_satellite_list(self.GLGSV.SatelliteList)

                elif "$BDGSV" in line:
                    if not self.BDGSV.decode(line):
                        continue

                    self.set_last_sentence(self.BDGSV.Sentence)
                    self.write_to_output_file(self.BDGSV.to_string())

                    navigate_data.set_bds_view(self.BDGSV.View)
                    navigate_data.set_bds_satellite_list(self.BDGSV.SatelliteList)

                elif "$GBGSV" in line:
                    if not self.GBGSV.decode(line):
                        continue

                    self.set_last_sentence(self.GBGSV.Sentence)
                    self.write_to_output_file(self.GBGSV.to_string())

                    navigate_data.set_bds_view(self.GBGSV.View)
                    navigate_data.set_bds_satellite_list(self.GBGSV.SatelliteList)

                elif "$GNGSV" in line:
                    if not self.GNGSV.decode(line):
                        continue

                    self.set_last_sentence(self.GNGSV.Sentence)
                    self.write_to_output_file(self.GNGSV.to_string())

                    navigate_data.set_view(self.GNGSV.View)
                    navigate_data.set_satellite_list(self.GNGSV.SatelliteList)

                elif "$GPGLL" in line:
                    if not self.GPGLL.decode(line):
                        continue

                    self.set_last_sentence(self.GPGLL.Sentence)
                    self.write_to_output_file(self.GPGLL.to_string())

                elif "$BDGLL" in line:
                    if not self.BDGLL.decode(line):
                        continue

                    self.set_last_sentence(self.BDGLL.Sentence)
                    self.write_to_output_file(self.BDGLL.to_string())

                elif "$GBGLL" in line:
                    if not self.GBGLL.decode(line):
                        continue

                    self.set_last_sentence(self.GBGLL.Sentence)
                    self.write_to_output_file(self.GBGLL.to_string())

                elif "$GNGLL" in line:
                    if not self.GNGLL.decode(line):
                        continue

                    self.set_last_sentence(self.GNGLL.Sentence)
                    self.write_to_output_file(self.GNGLL.to_string())

                self.add_to_navigate_data_list(navigate_data)

        self.nmea_statistic()

        self.NmeaFile.close()
        self.OutputFile.close()

    def set_last_sentence(self, sentence):
        if len(sentence) == 0:
            return

        self.LastSentence = sentence

        if self.NmeaFile is None:
            return

        self.NmeaFile.write(sentence + "\n")

    def write_to_output_file(self, text):
        if self.OutputFile is None:
            return

        if len(text) == 0:
            return

        self.OutputFile.write(text + "\n")

    def setup_date_time_from(self):
        if DATE_TIME_FROM is not None:
            self.DateTimeFrom = datetime.datetime.strptime(DATE_TIME_FROM, DATE_TIME_FORMAT)

    def setup_date_time_to(self):
        if DATE_TIME_TO is not None:
            self.DateTimeTo = datetime.datetime.strptime(DATE_TIME_TO, DATE_TIME_FORMAT)

    def check_date_time(self, navigate_data):
        result = False

        if navigate_data is None:
            return result

        navigate_data.setup_local_date_time()
        if navigate_data.LocalDateTime is None:
            return result

        if self.DateTimeFrom is not None:
            if navigate_data.LocalDateTime < self.DateTimeFrom:
                return result

        if self.DateTimeTo is not None:
            if navigate_data.LocalDateTime > self.DateTimeTo:
                return result

        result = True

        return result

    def add_to_navigate_data_list(self, navigate_data):
        if navigate_data is None:
            return

        if not self.check_date_time(navigate_data):
            return

        if navigate_data.LatitudeValue is None or navigate_data.LongitudeValue is None:
            return
        else:
            self.NavigateDataList.append(navigate_data)

            self.NmeaStatistic.add_to_data_list(navigate_data)

    def nmea_statistic(self):
        if self.NmeaStatistic is None:
            return

        self.NmeaStatistic.statistic()

        self.NmeaStatistic.draw()
