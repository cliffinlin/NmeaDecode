#!/usr/bin/env python

import sys
import webbrowser

import easygui

from FoliumMap import FoliumMap
from LogFile import LogFile
from NmeaDecode import NmeaDecode


def main():
    file_name = easygui.fileopenbox(msg="Log File", title="Open", default='*.txt')
    if file_name is None:
        print("Please select a file.")
        sys.exit()

    log_file = LogFile()
    log_file.set_file_name(file_name)
    log_file.sort()

    nmea_decode = NmeaDecode()
    nmea_decode.set_file_name(log_file.FileName, log_file.FileNameSorted)
    nmea_decode.decode()

    folium_map = FoliumMap()
    folium_map.set_file_name(log_file.FileName)
    folium_map.set_navigate_data_list(nmea_decode.NavigateDataList)
    folium_map.draw()
    webbrowser.open(folium_map.FileName)

    # gmplot_map = GMPlotMap()
    # gmplot_map.set_file_name(log_file.FileName)
    # gmplot_map.set_navigate_data_list(nmea_decode.NavigateDataList)
    # gmplot_map.draw()

    return 0


if __name__ == "__main__":
    main()
