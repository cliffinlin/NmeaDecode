#!/usr/bin/env python

import datetime

DEFAULT_ROUND_NDIGITS = 4
SEPARATE_STRING = " "


class NavigateData:
    def __init__(self):
        self.Separate = SEPARATE_STRING

        self.Date = ""
        self.Year = None
        self.Month = None
        self.Day = None

        self.Time = ""
        self.Hour = None
        self.Minute = None
        self.Second = None

        self.Latitude = ""
        self.LatitudeValue = None
        self.Longitude = ""
        self.LongitudeValue = None
        self.Altitude = ""

        self.SpeedM = ""

        self.FixType = ""

        self.GPSView = ""
        self.GPSUsed = ""

        self.BDSView = ""
        self.BDSUsed = ""

        self.PDOP = ""
        self.HDOP = ""
        self.VDOP = ""

    def get_datetime(self):
        result = None

        if self.Hour is None or self.Minute is None or self.Second is None:
            return result

        result = datetime.datetime.strptime(self.Hour + ":" + self.Minute + ":" + self.Second[0:2], '%H:%M:%S')
        return result

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

    def set_speed_m(self, speed_m):
        self.SpeedM = speed_m

    def set_fix_type(self, fix_type):
        self.FixType = fix_type

    def set_gps_view(self, gps_view):
        self.GPSView = gps_view

    def set_gps_used(self, gps_used):
        self.GPSUsed = gps_used

    def set_bds_view(self, bds_view):
        self.BDSView = bds_view

    def set_bds_used(self, bds_used):
        self.BDSUsed = bds_used

    def set_pdop(self, pdop):
        self.PDOP = pdop

    def set_hdop(self, hdop):
        self.HDOP = hdop

    def set_vdop(self, vdop):
        self.VDOP = vdop

    def date_time_to_string(self):
        result = ""

        if self.Year is None or self.Month is None or self.Day is None or self.Hour is None or self.Minute is None or self.Second is None:
            return result

        utc_datetime = datetime.datetime.strptime(
            self.Year + "-" + self.Month + "-" + self.Day + " " + self.Hour + ":" + self.Minute + ":" + self.Second,
            '%Y-%m-%d %H:%M:%S.%f')
        local_datetime = utc_datetime + datetime.timedelta(hours=8)

        result += local_datetime.strftime('%Y-%m-%d %H:%M:%S')
        result += self.Separate

        return result

    def latitude_to_string(self):
        result = ""

        if self.LatitudeValue is None:
            return result

        result += str(self.LatitudeValue)
        result += self.Separate

        return result

    def longitude_to_string(self):
        result = ""
        if self.LongitudeValue is None:
            return result

        result += str(self.LongitudeValue)
        result += self.Separate

        return result

    def altitude_to_string(self):
        result = ""

        if len(self.Altitude) == 0:
            return result

        result += "Altitude="
        result += self.Altitude + "M"
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

    def fix_type_to_string(self):
        result = ""

        if len(self.FixType) == 0:
            return result

        result += "FixType="

        value = int(self.FixType)
        if value == 1:
            result += "NoFix"
        elif value == 2:
            result += "2DFix"
        elif value == 3:
            result += "3DFix"

        result += self.Separate

        return result

    def gps_view_to_string(self):
        result = ""

        if len(self.GPSView) == 0:
            return result

        result += "GPSView="
        result += self.GPSView
        result += self.Separate

        return result

    def bds_view_to_string(self):
        result = ""

        if len(self.BDSView) == 0:
            return result

        result += "BDSView="
        result += self.BDSView
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

    def to_string(self):
        result = ""

        result += self.date_time_to_string()
        result += self.latitude_to_string()
        result += self.longitude_to_string()
        result += self.altitude_to_string()
        result += self.speed_m_to_string()
        result += self.fix_type_to_string()
        result += self.gps_view_to_string()
        result += self.bds_view_to_string()
        result += self.pdop_to_string()
        result += self.hdop_to_string()
        result += self.vdop_to_string()

        return result
