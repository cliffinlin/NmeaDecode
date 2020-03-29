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

        self.PDOP = ""
        self.HDOP = ""
        self.VDOP = ""

        self.SpeedM = ""

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

    def set_pdop(self, pdop):
        self.PDOP = pdop

    def set_hdop(self, hdop):
        self.HDOP = hdop

    def set_vdop(self, vdop):
        self.VDOP = vdop

    def set_speed_m(self, speed_m):
        self.SpeedM = speed_m

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

    def speed_m_to_string(self):
        result = ""

        if len(self.SpeedM) == 0:
            return result

        result += self.SpeedM + "KM"
        result += self.Separate

        return result

    def to_string(self):
        result = ""

        result += self.date_time_to_string()
        result += self.latitude_to_string()
        result += self.longitude_to_string()
        result += self.speed_m_to_string()

        return result
