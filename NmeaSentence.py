#!/usr/bin/env python

SEPARATE_STRING = ",\t"

DATE_STRING_LENGTH_MIN = 6
DATE_STRING_DAY_INDEX_MIN = 0
DATE_STRING_DAY_INDEX_MAX = 2
DATE_STRING_MONTH_INDEX_MIN = 2
DATE_STRING_MONTH_INDEX_MAX = 4
DATE_STRING_YEAR_INDEX_MIN = 4

TIME_STRING_LENGTH_MIN = 6
TIME_STRING_HOUR_INDEX_MIN = 0
TIME_STRING_HOUR_INDEX_MAX = 2
TIME_STRING_MINUTE_INDEX_MIN = 2
TIME_STRING_MINUTE_INDEX_MAX = 4
TIME_STRING_SECOND_INDEX_MIN = 4

LATITUDE_STRING_LENGTH_MIN = 4
LATITUDE_STRING_DEGREE_INDEX_MIN = 0
LATITUDE_STRING_DEGREE_INDEX_MAX = 2
LATITUDE_STRING_MINUTE_INDEX_MIN = 2

LONGITUDE_STRING_LENGTH_MIN = 5
LONGITUDE_STRING_DEGREE_INDEX_MIN = 0
LONGITUDE_STRING_DEGREE_INDEX_MAX = 3
LONGITUDE_STRING_MINUTE_INDEX_MAX = 3


class NmeaSentence:
    def __init__(self):
        self.Separate = SEPARATE_STRING

        self.Sentence = ""
        self.DataType = ""
        self.Checksum = ""
        self.Data = []

        self.Date = ""
        self.Time = ""

        self.Latitude = ""
        self.LatitudeDirection = ""
        self.Longitude = ""
        self.LongitudeDirection = ""
        self.Altitude = ""
        self.AltitudeUnit = ""

        self.PDOP = ""
        self.HDOP = ""
        self.VDOP = ""

        self.Status = ""

        self.SpeedN = ""
        self.SpeedM = ""

    def decode(self, line):
        self.Sentence = ""
        self.Data = None

        if line is None:
            return

        index = line.find(self.DataType)
        if index == -1:
            return

        nmea_line = line[index:]

        nmea_line = nmea_line.strip()
        if nmea_line is None:
            return

        list_a = nmea_line.split("*")
        if list_a is None:
            return

        if len(list_a) < 2:
            return

        self.Sentence = nmea_line

        self.Checksum = list_a[1]

        list_b = list_a[0].split(",")
        if list_b is None:
            return

        if len(list_b) < 2:
            return

        self.DataType = list_b[0]
        self.Data = list_b[1:]

    def date_to_string(self):
        result = ""

        date = self.Date.strip()
        if date is None:
            return result
        if len(date) < DATE_STRING_LENGTH_MIN:
            return result

        day = date[DATE_STRING_DAY_INDEX_MIN:DATE_STRING_DAY_INDEX_MAX]
        month = date[DATE_STRING_MONTH_INDEX_MIN:DATE_STRING_MONTH_INDEX_MAX]
        year = date[DATE_STRING_YEAR_INDEX_MIN:]

        if len(year) == 2:
            year = "20" + year

        result += "Date:"
        result += year + "-" + month + "-" + day
        result += self.Separate

        return result

    def time_to_string(self):
        result = ""

        time = self.Time.strip()
        if time is None:
            return result
        if len(time) < TIME_STRING_LENGTH_MIN:
            return result

        hour = time[TIME_STRING_HOUR_INDEX_MIN:TIME_STRING_HOUR_INDEX_MAX]
        minute = time[TIME_STRING_MINUTE_INDEX_MIN:TIME_STRING_MINUTE_INDEX_MAX]
        second = time[TIME_STRING_SECOND_INDEX_MIN:]

        result += "Time:"
        result += hour + ":" + minute + ":" + second
        result += self.Separate

        return result

    def latitude_to_string(self):
        result = ""

        if len(self.Latitude) < LATITUDE_STRING_LENGTH_MIN:
            return result

        degree = self.Latitude[LATITUDE_STRING_DEGREE_INDEX_MIN:LATITUDE_STRING_DEGREE_INDEX_MAX]
        minute = self.Latitude[LATITUDE_STRING_MINUTE_INDEX_MIN:]

        result += "Latitude="
        result += degree + "\'" + minute + "\"" + self.LatitudeDirection
        result += self.Separate

        return result

    def longitude_to_string(self):
        result = ""

        if len(self.Longitude) < LONGITUDE_STRING_LENGTH_MIN:
            return result

        degree = self.Longitude[LONGITUDE_STRING_DEGREE_INDEX_MIN:LONGITUDE_STRING_DEGREE_INDEX_MAX]
        minute = self.Longitude[LONGITUDE_STRING_MINUTE_INDEX_MAX:]

        result += "Longitude="
        result += degree + "\'" + minute + "\"" + self.LongitudeDirection
        result += self.Separate

        return result

    def altitude_to_string(self):
        result = ""

        if len(self.Altitude) == 0:
            return result

        result += "Altitude="
        result += self.Altitude + self.AltitudeUnit
        result += self.Separate

        return result

    def pdop_to_string(self):
        result = ""

        if len(self.PDOP) == 0:
            return result

        result += "PDOP="
        result += self.PDOP
        result += self.Separate

        return result

    def hdop_to_string(self):
        result = ""

        if len(self.HDOP) == 0:
            return result

        result += "HDOP="
        result += self.HDOP
        result += self.Separate

        return result

    def vdop_to_string(self):
        result = ""

        if len(self.VDOP) == 0:
            return result

        result += "VDOP="
        result += self.VDOP
        result += self.Separate

        return result

    def status_to_string(self):
        result = ""

        if len(self.Status) == 0:
            return result

        result += "Status:"

        if "A" in self.Status:
            result += "Active"
        elif "V" in self.Status:
            result += "Void"

        result += self.Separate

        return result

    def speed_n_to_string(self):
        result = ""

        if len(self.SpeedN) == 0:
            return result

        result += "Speed="
        result += self.SpeedN + "KN"
        result += self.Separate

        return result

    def speed_m_to_string(self):
        result = ""

        if len(self.SpeedM) == 0:
            return result

        result += "Speed="
        result += self.SpeedM + "KM"
        result += self.Separate

        return result

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        # result += self.Sentence + self.Separate
        result += self.DataType + self.Separate

        return result
