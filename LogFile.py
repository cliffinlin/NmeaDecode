#!/usr/bin/env python
import os
from datetime import datetime

KEY_WORD_MAIN_LOG = "main_log"


class LogFile:
    def __init__(self):
        self.InputFile = None
        self.OutputFile = None
        self.OutputFileName = ""

        self.Date = None
        self.Time = None

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

    def sort(self, input_file_name, output_file_name):
        if not os.path.exists(input_file_name):
            print(input_file_name, "file not found!")
            return

        line_list = []
        with open(input_file_name) as self.InputFile:
            for line in self.InputFile:
                self.Date = None
                self.Time = None

                self.parse_date_time(line)
                if self.Date is None or self.Time is None:
                    continue

                line_list.append(line)

        self.OutputFile = open(output_file_name, "w")

        if len(line_list) > 0:
            print("Sorting line list, waiting...")
            sorted_line_list = sorted(line_list, key=self.key_function)

        if self.OutputFile is not None:
            for line in sorted_line_list:
                self.OutputFile.write(line)

        if self.OutputFile is not None:
            self.OutputFile.close()
