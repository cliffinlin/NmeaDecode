#!/usr/bin/env python
# sample NMEA sentence:
# $GNRMC,075414.000,A,4004.680961,N,11614.576639,E,0.031,0.00,240320,,E,A*08
#
# $GNVTG,0.00,T,,M,0.031,N,0.058,K,A*2C
#
# $GNGGA,075414.000,4004.680961,N,11614.576639,E,1,14,0.89,30.372,M,0,M,,*65
#
# $GPGSA,A,3,01,07,08,11,27,28,30,,,,,,1.51,0.89,1.22*05
#
# $BDGSA,A,3,01,03,04,07,08,10,13,,,,,,1.51,0.89,1.22*1C
#
# $GPGSV,3,1,09,01,45,166,44,07,64,246,46,08,55,042,45,11,77,113,43*7F
#
# $GPGSV,3,2,09,20,,,22,22,,,21,27,23,055,26,28,18,296,36*7B
#
# $GPGSV,3,3,09,30,44,299,43*46
#
# $BDGSV,3,1,10,01,38,144,39,02,31,223,00,03,43,188,41,04,26,123,39*63
#
# $BDGSV,3,2,10,05,14,246,00,07,76,070,41,08,42,172,40,09,10,210,00*69
#
# $BDGSV,3,3,10,10,71,319,41,13,21,189,41*64
#
# $GNGLL,4004.680961,N,11614.576639,E,075414.000,A,A*4F

import os
import folium

from BDGGA import BDGGA
from BDGLL import BDGLL
from BDGSA import BDGSA
from BDGSV import BDGSV
from BDRMC import BDRMC
from BDVTG import BDVTG
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

FILE_NAME_LOG = "log.txt"
FILE_NAME_LOG_SORTED = "sorted.txt"
FILE_NAME_OUTPUT = "nmea.out"
FILE_NAME_MAP_VIEW = 'index.html'

MAP_DEFAULT_LOCATION = [39.9032, 116.3915]
MAP_DEFAULT_ZOOM_START = 12

MAP_DRAW_LINE = True
MAP_DRAW_MARK = True

SAMPLE_DURATION_IN_SECOND = 1

DOP_THRESH_HOLD = 5


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

        self.LastDateTime = None

        self.InputFileName = FILE_NAME_LOG_SORTED
        self.InputFile = None

        self.OutputFileName = FILE_NAME_OUTPUT
        self.OutputFile = None

        self.Map = folium.Map(
            location = MAP_DEFAULT_LOCATION,
            zoom_start = MAP_DEFAULT_ZOOM_START
        )
        self.Map.add_child(folium.LatLngPopup())

    def decode(self):
        if not os.path.exists(self.InputFileName):
            print(self.InputFileName, "file not found!")
            return

        self.OutputFile = open(self.OutputFileName, "w")

        with open(self.InputFileName) as self.InputFile:
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

        date_time_now = navigate_data.get_local_date_time()
        if date_time_now is None:
            return

        if self.LastDateTime is not None:
            duration = date_time_now - self.LastDateTime
            if duration.seconds < SAMPLE_DURATION_IN_SECOND:
                return

        self.LastDateTime = date_time_now

        if navigate_data.LatitudeValue is None or navigate_data.LongitudeValue is None:
            return
        else:
            self.NavigateDataList.append(navigate_data)

    def draw(self):
        print("\n")
        print("Prepare data to draw...")
        if self.NavigateDataList is None or len(self.NavigateDataList) == 0:
            print("No data to draw!")
            return

        location_list = []
        for navigate_data in self.NavigateDataList:
            if navigate_data is None:
                continue

            if navigate_data.LatitudeValue is None or navigate_data.LongitudeValue is None:
                continue

            location = [navigate_data.LatitudeValue, navigate_data.LongitudeValue]
            location_list.append(location)

            if MAP_DRAW_MARK:
                if float(navigate_data.PDOP) > DOP_THRESH_HOLD:
                    folium.Marker(location=location,
                                  popup=navigate_data.to_string(),
                                  icon=folium.Icon(color='red', icon='info-sign')).add_to(self.Map)
                else:
                    folium.Marker(location=location,
                              popup=navigate_data.to_string()).add_to(self.Map)

        if MAP_DRAW_LINE:
            folium.PolyLine(locations=location_list).add_to(self.Map)

        print("Save map data ...")
        self.Map.save(FILE_NAME_MAP_VIEW)
        print("Map saved in " + FILE_NAME_MAP_VIEW)


def main():
    log_file = LogFile()
    log_file.sort(FILE_NAME_LOG, FILE_NAME_LOG_SORTED)

    nmea_decode = NmeaDecode()
    nmea_decode.decode()
    nmea_decode.draw()
    return 0


if __name__ == "__main__":
    main()
