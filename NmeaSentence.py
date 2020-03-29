#!/usr/bin/env python

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

DEFAULT_ROUND_NDIGITS = 4
SEPARATE_STRING = ",\t"

class NmeaSentence:
    def __init__(self):
        self.Separate = SEPARATE_STRING

        self.Sentence = ""
        self.DataType = ""
        self.Checksum = ""
        self.Data = None

        self.Date = ""
        self.Year = None
        self.Month = None
        self.Day = None

        self.Time = ""
        self.Hour = None
        self.Minute = None
        self.Second = None

        self.Latitude = ""
        self.LatitudeDirection = ""
        self.LatitudeValue = None
        self.Longitude = ""
        self.LongitudeDirection = ""
        self.LongitudeValue = None
        self.Altitude = ""
        self.AltitudeUnit = ""

        self.PDOP = ""
        self.HDOP = ""
        self.VDOP = ""

        self.Status = ""

        self.SpeedN = ""
        self.SpeedM = ""

    def decode(self, line):
        self.__init__()

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

    def decode_date(self):
        if self.Date is None:
            return

        date = self.Date.strip()
        if date is None:
            return
        if len(date) < DATE_STRING_LENGTH_MIN:
            return

        self.Day = date[DATE_STRING_DAY_INDEX_MIN:DATE_STRING_DAY_INDEX_MAX]
        self.Month = date[DATE_STRING_MONTH_INDEX_MIN:DATE_STRING_MONTH_INDEX_MAX]
        self.Year = date[DATE_STRING_YEAR_INDEX_MIN:]

        if len(self.Year) == 2:
            self.Year = "20" + self.Year

    def date_to_string(self):
        result = ""

        if self.Year is None or self.Month is None or self.Day is None:
            return result

        result += "Date:"
        result += self.Year + "-" + self.Month + "-" + self.Day
        result += self.Separate

        return result

    def decode_time(self):
        if self.Time is None:
            return

        time = self.Time.strip()
        if time is None:
            return
        if len(time) < TIME_STRING_LENGTH_MIN:
            return

        self.Hour = time[TIME_STRING_HOUR_INDEX_MIN:TIME_STRING_HOUR_INDEX_MAX]
        self.Minute = time[TIME_STRING_MINUTE_INDEX_MIN:TIME_STRING_MINUTE_INDEX_MAX]
        self.Second = time[TIME_STRING_SECOND_INDEX_MIN:]

    def time_to_string(self):
        result = ""

        if self.Hour is None or self.Minute is None or self.Second is None:
            return result

        result += "Time:"
        result += self.Hour + ":" + self.Minute + ":" + self.Second
        result += self.Separate

        return result

    def decode_latitude(self):
        if self.Latitude is None or self.LatitudeDirection is None:
            return

        if len(self.Latitude) < LATITUDE_STRING_LENGTH_MIN:
            return

        degree = self.Latitude[LATITUDE_STRING_DEGREE_INDEX_MIN:LATITUDE_STRING_DEGREE_INDEX_MAX]
        minute = self.Latitude[LATITUDE_STRING_MINUTE_INDEX_MIN:]

        self.LatitudeValue = float(degree) + float(minute) / 60.0

        if self.LatitudeDirection == "S":
            self.LatitudeValue = -1 * self.LatitudeValue

    def latitude_to_string(self):
        result = ""

        if self.LatitudeValue is None:
            return result

        result += "Latitude="
        result += str(self.LatitudeValue)
        result += self.Separate

        return result

    def decode_longitude(self):
        if self.Longitude is None or self.LongitudeDirection is None:
            return

        if len(self.Longitude) < LONGITUDE_STRING_LENGTH_MIN:
            return

        degree = self.Longitude[LONGITUDE_STRING_DEGREE_INDEX_MIN:LONGITUDE_STRING_DEGREE_INDEX_MAX]
        minute = self.Longitude[LONGITUDE_STRING_MINUTE_INDEX_MAX:]

        self.LongitudeValue = float(degree) + float(minute) / 60.0

        if self.LongitudeDirection == "W":
            self.LongitudeValue = -1 * self.Longitude

    def longitude_to_string(self):
        result = ""
        if self.LongitudeValue is None:
            return result

        result += "Longitude="
        result += str(self.LongitudeValue)
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
