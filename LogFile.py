#!/usr/bin/env python
import os
import sys
from datetime import datetime

FILE_NAME_EXT_SORTED = ".sorted"

KEY_WORD_MAIN_LOG = "main_log"


class LogFile:
    def __init__(self):
        self.FileName = None
        self.FileNameSorted = None

        self.InputFile = None
        self.OutputFile = None

        self.Date = None
        self.Time = None

    def set_file_name(self, file_name):
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

    def sort(self):
        if not os.path.exists(self.FileName):
            print(self.FileName, "file not found!")
            sys.exit()

        line_list = []
        with open(self.FileName, encoding='latin1') as self.InputFile:
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
            sorted_line_list = sorted(line_list, key=self.key_function)

        if self.OutputFile is not None:
            for line in sorted_line_list:
                self.OutputFile.write(line)

        if self.OutputFile is not None:
            self.OutputFile.close()
