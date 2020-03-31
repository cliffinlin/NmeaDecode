#!/usr/bin/env python
import datetime

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

DEFAULT_TIME_ZONE = 8
DEFAULT_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


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

        self.FixQuality = ""
        self.TrackedNumber = ""

        self.Selection = ""
        self.FixType = ""

        self.View = ""

        self.Used = None

        self.SatelliteList = []

        self.PDOP = ""
        self.HDOP = ""
        self.VDOP = ""

        self.Status = ""

        self.TrueTrack = ""
        self.TrueTrackMark = ""
        self.MagneticTrack = ""
        self.MagneticTrackMark = ""
        self.SpeedN = ""
        self.SpeedNMark = ""
        self.SpeedM = ""
        self.SpeedMMark = ""

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

    def set_date(self, date, day, month, year):
        self.Date = date
        self.Day = day
        self.Month = month
        self.Year = year

    def set_time(self, time, hour, minute, second):
        self.Time = time
        self.Hour = hour
        self.Minute = minute
        self.Second = second

    def set_latitude(self, latitude, latitudeValue):
        self.Latitude = latitude
        self.LatitudeValue = latitudeValue

    def set_longitude(self, longitude, longitudeValue):
        self.Longitude = longitude
        self.LongitudeValue = longitudeValue

    def set_altitude(self, altitude):
        self.Altitude = altitude

    def set_fix_quality(self, fix_quality):
        self.FixQuality = fix_quality

    def set_tracked_number(self, tracked_number):
        self.TrackedNumber = tracked_number

    def set_speed_n(self, speed_n):
        self.SpeedN = speed_n

    def set_speed_m(self, speed_m):
        self.SpeedM = speed_m

    def set_fix_type(self, fix_type):
        self.FixType = fix_type

    def set_satellite_list(self, satellite_list):
        if satellite_list is None:
            return
        self.SatelliteList = satellite_list

    def set_pdop(self, pdop):
        self.PDOP = pdop

    def set_hdop(self, hdop):
        self.HDOP = hdop

    def set_vdop(self, vdop):
        self.VDOP = vdop

    def get_utc_date_time(self):
        result = None

        if self.Year is None or self.Month is None or self.Day is None or self.Hour is None or self.Minute is None or self.Second is None:
            return result

        result = datetime.datetime.strptime(
            self.Year + "-" + self.Month + "-" + self.Day + " " + self.Hour + ":" + self.Minute + ":" + self.Second,
            DEFAULT_DATE_TIME_FORMAT)

        return result

    def get_local_date_time(self):
        result = None

        utc_date_time = self.get_utc_date_time()

        if utc_date_time is None:
            return result

        result = utc_date_time + datetime.timedelta(hours=DEFAULT_TIME_ZONE)

        return result

    def utc_date_time_to_string(self):
        result = ""

        if self.Year is None or self.Month is None or self.Day is None or self.Hour is None or self.Minute is None or self.Second is None:
            return result

        utc_date_time = self.get_utc_date_time()
        if utc_date_time is None:
            return result

        result += utc_date_time.strftime(DEFAULT_DATE_TIME_FORMAT)
        result += self.Separate

        return result

    def local_date_time_to_string(self):
        result = ""

        local_date_time = self.get_local_date_time()
        if local_date_time is None:
            return result

        result += local_date_time.strftime(DEFAULT_DATE_TIME_FORMAT)
        result += self.Separate

        return result

    def date_to_string(self):
        result = ""

        if self.Year is None or self.Month is None or self.Day is None:
            return result

        result += "Date:"
        result += self.Year + "-" + self.Month + "-" + self.Day
        result += self.Separate

        return result

    def time_to_string(self):
        result = ""

        if self.Hour is None or self.Minute is None or self.Second is None:
            return result

        result += "Time:"
        result += self.Hour + ":" + self.Minute + ":" + self.Second
        result += self.Separate

        return result

    def latitude_to_string(self):
        result = ""

        if self.LatitudeValue is None:
            return result

        result += "Latitude="
        result += str(self.LatitudeValue)
        result += self.Separate

        return result

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

        if self.Altitude is None or len(self.Altitude) == 0:
            return result

        result += "Altitude="
        result += self.Altitude + self.AltitudeUnit
        result += self.Separate

        return result

    def fix_quality_to_string(self):
        result = ""
        remark = ""

        if self.FixQuality is None or len(self.FixQuality) == 0:
            return result

        value = int(self.FixQuality)

        if value == 0:
            remark = "Invalid"
        elif value == 1:
            remark = "SPS"
        elif value == 2:
            remark = "DGPS"
        elif value == 3:
            remark = "PPS"
        elif value == 4:
            remark = "RTK"
        elif value == 5:
            remark = "Float RTK"
        elif value == 6:
            remark = "Estimated"

        if len(remark) == 0:
            return result

        result = "FixQuality:"
        result += remark
        result += self.Separate

        return result

    def tracked_number_to_string(self):
        result = ""

        if len(self.TrackedNumber) == 0:
            return result

        result += "TrackedNumber="
        result += self.TrackedNumber
        result += self.Separate

        return result

    def selection_to_string(self):
        result = ""

        if self.Selection is None or len(self.Selection) == 0:
            return result

        result += "Selection:"
        if "A" in self.Selection:
            result += "Auto"
        elif "M" in self.Selection:
            result += "Manual"

        result += self.Separate

        return result

    def fix_type_to_string(self):
        result = ""

        if self.FixType is None or len(self.FixType) == 0:
            return result

        result += "FixType="

        value = int(self.FixType)
        if value == 1:
            result += "NoFix"
        elif value == 2:
            result += "2D"
        elif value == 3:
            result += "3D"

        result += self.Separate

        return result

    def view_to_string(self):
        result = ""

        if self.View is None or len(self.View) == 0:
            return result

        result += "View="
        result += self.View
        result += self.Separate

        return result

    def used_to_string(self):
        result = ""

        if self.Used is None or len(self.Used) == 0:
            return result

        result += "Used:"

        count = 0
        for prn in self.Used:
            if prn is not None and len(prn) > 0:
                if count == 0:
                    result += "#" + prn
                else:
                    result += "," + "#" + prn
            count += 1

        result += self.Separate

        return result

    def satellite_list_to_string(self):
        result = ""

        if self.SatelliteList is None or len(self.SatelliteList) == 0:
            return result

        for satellite in self.SatelliteList:
            if satellite is not None:
                result += satellite.to_string()

        return result

    def pdop_to_string(self):
        result = ""

        if self.PDOP is None or len(self.PDOP) == 0:
            return result

        result += "PDOP="
        result += self.PDOP
        result += self.Separate

        return result

    def hdop_to_string(self):
        result = ""

        if self.HDOP is None or len(self.HDOP) == 0:
            return result

        result += "HDOP="
        result += self.HDOP
        result += self.Separate

        return result

    def vdop_to_string(self):
        result = ""

        if self.VDOP is None or len(self.VDOP) == 0:
            return result

        result += "VDOP="
        result += self.VDOP
        result += self.Separate

        return result

    def status_to_string(self):
        result = ""

        if self.Status is None or len(self.Status) == 0:
            return result

        result += "Status:"

        if "A" in self.Status:
            result += "Active"
        elif "V" in self.Status:
            result += "Void"

        result += self.Separate

        return result

    def true_track_to_string(self):
        result = ""

        if len(self.TrueTrack) == 0:
            return result

        result += "TrueTrack="
        result += self.TrueTrack
        result += self.Separate

        return result

    def magnetic_track_to_string(self):
        result = ""

        if len(self.MagneticTrack) == 0:
            return result

        result += "MagneticTrack="
        result += self.MagneticTrack
        result += self.Separate

        return result

    def speed_n_to_string(self):
        result = ""

        if self.SpeedN is None or len(self.SpeedN) == 0:
            return result

        result += "Speed="
        result += self.SpeedN + "KN"
        result += self.Separate

        return result

    def speed_m_to_string(self):
        result = ""

        if self.SpeedM is None or len(self.SpeedM) == 0:
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
