#!/usr/bin/env python
import configparser
import os
import sys
from datetime import datetime
import easygui

DEFAULT_ENCODING = "latin1"

CONFIG_FILE_NAME = "config.ini"
CONFIG_SECTION_DEFAULT = "DEFAULT"
CONFIG_OPTION_NORM_PATH = "norm_path"
CONFIG_OPTION_NORM_PATH_VALUE = '~/Downloads'

FILE_NAME_EXT = ".txt"
FILE_NAME_EXT_SORTED = ".sorted"

FILE_TYPE_MAIN_LOG = "main_log"
FILE_TYPE_NMEA_LOG = "nmea"

KEY_WORD_NMEA_DATA_TYPE = ["RMC", "VTG", "GGA", "GSA", "GSV", "GLL"]


class LogFile:
    def __init__(self):
        self.DefaultNormPath = None
        self.NormPath = None

        self.FileName = None
        self.FileNameSorted = None

        self.InputFile = None
        self.OutputFile = None

        self.Date = None
        self.Time = None

        self.FileType = FILE_TYPE_MAIN_LOG

        self.KeyWords = KEY_WORD_NMEA_DATA_TYPE

        self.select_dir()
        self.search_nmea()
        self.sort_line_list()

    def get_default_norm_path(self):
        config = configparser.ConfigParser()

        if not os.path.exists(CONFIG_FILE_NAME):
            self.NormPath = CONFIG_OPTION_NORM_PATH_VALUE
            return

        config.read(CONFIG_FILE_NAME)

        if not config.has_option(CONFIG_SECTION_DEFAULT, CONFIG_OPTION_NORM_PATH):
            self.NormPath = CONFIG_OPTION_NORM_PATH_VALUE
            return

        self.NormPath = config[CONFIG_SECTION_DEFAULT][CONFIG_OPTION_NORM_PATH]

        if not os.path.exists(self.NormPath):
            self.NormPath = CONFIG_OPTION_NORM_PATH_VALUE

    def set_default_norm_path(self):
        config = configparser.ConfigParser()

        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config[CONFIG_SECTION_DEFAULT][CONFIG_OPTION_NORM_PATH] = self.NormPath
            config.write(configfile)

    def select_dir(self):
        self.get_default_norm_path()

        normpath = easygui.diropenbox(msg="Log Dir", title="Select", default=self.NormPath)
        if normpath is None:
            print("No dir selected.")
            return

        self.NormPath = normpath
        self.FileName = self.NormPath + FILE_NAME_EXT
        self.FileNameSorted = self.FileName + FILE_NAME_EXT_SORTED

        self.set_default_norm_path()

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
                self.parse_year(part_list[-3])

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

        try:
            local_datetime = datetime.strptime(self.Date + " " + self.Time, '%Y-%m-%d %H:%M:%S.%f')
            diff_seconds = (local_datetime - datetime.fromtimestamp(0)).total_seconds()
        except ValueError as e:
            print("ValueError:", e)
            return 0

        return diff_seconds

    def sort_line_list(self):
        if self.FileName is None:
            return

        if os.path.exists(self.FileNameSorted):
            print(self.FileNameSorted, "already exist.")
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

                if FILE_TYPE_MAIN_LOG in line:
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

        if os.path.exists(self.FileName):
            print(self.FileName, "already exist.")
            return

        self.OutputFile = open(self.FileName, "w")

        root_dir = self.NormPath

        for root, dirs, files in os.walk(root_dir, onerror=None):
            for filename in files:
                if FILE_TYPE_NMEA_LOG in filename:
                    self.FileType = FILE_TYPE_NMEA_LOG

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
