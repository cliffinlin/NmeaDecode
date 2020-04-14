#!/usr/bin/env python
import os
import sys
from datetime import datetime
import easygui

DEFAULT_ENCODING = "latin1"

FILE_NAME_EXT = ".txt"
FILE_NAME_EXT_SORTED = ".sorted"

KEY_WORD_MAIN_LOG = "main_log"
KEY_WORD_NMEA_DATA_TYPE = ["RMC", "VTG", "GGA", "GSA", "GSV", "GLL"]


class LogFile:
    def __init__(self):
        self.NormPath = None

        self.FileName = None
        self.FileNameSorted = None

        self.InputFile = None
        self.OutputFile = None

        self.Date = None
        self.Time = None

        self.KeyWords = KEY_WORD_NMEA_DATA_TYPE

        self.select_dir()
        self.search_nmea()
        self.sort_line_list()

    def select_dir(self):
        normpath = easygui.diropenbox(msg="Log Dir", title="Select", default='~/Downloads')
        if normpath is None:
            print("No dir selected.")
            return

        self.NormPath = normpath
        self.FileName = self.NormPath + FILE_NAME_EXT
        self.FileNameSorted = self.NormPath + FILE_NAME_EXT_SORTED

    def select_file(self):
        file_name = easygui.fileopenbox(msg="Log File", title="Open", default='*.txt')
        if file_name is None:
            print("No file selected.")
            return

        self.FileName = file_name
        self.FileNameSorted = self.FileName + FILE_NAME_EXT_SORTED

    def parse_date_time(self, line):
        self.Date = None
        self.Time = None

        if line is None:
            return

        if KEY_WORD_MAIN_LOG not in line:
            return

        part_list = line.split(" ")
        if part_list is None:
            return

        if len(part_list) > 2:
            self.Time = part_list[1]

        self.parse_month_day(part_list[0])

    def parse_month_day(self, line):
        if line is None:
            return

        if len(line) > 0:
            part_list = line.split(":")
            if len(part_list) > 2:
                self.Date = part_list[-1]
                self.parse_year(part_list[0])

    def parse_year(self, line):
        if line is None:
            return

        if len(line) > 0:
            part_list = line.split("_")
            if len(part_list) > 3:
                self.Date = part_list[-3] + "-" + self.Date

    def key_function(self, line):
        if line is None:
            return 0

        self.parse_date_time(line)
        if self.Date is None or self.Time is None:
            return 0

        local_datetime = datetime.strptime(self.Date + " " + self.Time, '%Y-%m-%d %H:%M:%S.%f')
        diff_seconds = (local_datetime - datetime.fromtimestamp(0)).total_seconds()

        return diff_seconds

    def sort_line_list(self):
        if self.FileName is None:
            return

        if not os.path.exists(self.FileName):
            print(self.FileName, "file not found!")
            sys.exit()

        line_list = []
        line_list_sorted = []
        with open(self.FileName, encoding=DEFAULT_ENCODING) as self.InputFile:
            for line in self.InputFile:
                self.Date = None
                self.Time = None

                self.parse_date_time(line)
                if self.Date is None or self.Time is None:
                    continue

                line_list.append(line)

        self.OutputFile = open(self.FileNameSorted, "w")

        if len(line_list) > 0:
            print("Sorting line list, waiting...")
            line_list_sorted = sorted(line_list, key=self.key_function)

        if self.OutputFile is not None:
            for line in line_list_sorted:
                self.OutputFile.write(line)

        if self.OutputFile is not None:
            self.OutputFile.close()

    def search_nmea(self):
        if self.FileName is None:
            return

        self.OutputFile = open(self.FileName, "w")

        root_dir = self.NormPath

        for root, dirs, files in os.walk(root_dir, onerror=None):
            for filename in files:
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "rb") as f:
                        for i, line in enumerate(f):
                            try:
                                line = line.decode(DEFAULT_ENCODING)
                            except ValueError:
                                continue

                            if any(key_word in line for key_word in self.KeyWords):
                                output_line = file_path + ":" + str(i + 1) + ":" + line

                                print(output_line)

                                if self.OutputFile is not None:
                                    self.OutputFile.write(output_line)
                except (IOError, OSError):
                    pass

        if self.OutputFile is not None:
            self.OutputFile.close()
