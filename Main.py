#!/usr/bin/env python
import sys
import webbrowser

from FoliumMap import FoliumMap
from LogFile import LogFile
from NmeaDecode import NmeaDecode


def main():
    folium_map = FoliumMap()

    log_file = LogFile()
    if log_file.FileName is None:
        sys.exit()

    folium_map.set_file_name(log_file.FileName)

    nmea_decode = NmeaDecode()
    nmea_decode.set_file_name(log_file.FileName, log_file.FileNameSorted)
    nmea_decode.decode()
    folium_map.add_navigate_data_list(nmea_decode)

    # log_file = LogFile()
    # if log_file.FileName is not None:
    #     nmea_decode = NmeaDecode()
    #     nmea_decode.set_file_name(log_file.FileName, log_file.FileNameSorted)
    #     nmea_decode.decode()
    #     folium_map.add_navigate_data_list(nmea_decode, color="red")
    #
    # log_file = LogFile()
    # if log_file.FileName is not None:
    #     nmea_decode = NmeaDecode()
    #     nmea_decode.set_file_name(log_file.FileName, log_file.FileNameSorted)
    #     nmea_decode.decode()
    #     folium_map.add_navigate_data_list(nmea_decode, color="yellow")

    if len(folium_map.LocationList) > 0:
        folium_map.save()
        webbrowser.open(folium_map.FileName)

    # gmplot_map = GMPlotMap()
    # gmplot_map.set_file_name(log_file.FileName)
    # gmplot_map.set_navigate_data_list(nmea_decode.NavigateDataList)
    # gmplot_map.draw()

    return 0


if __name__ == "__main__":
    main()
