#!/usr/bin/env python

from NmeaSentence import NmeaSentence

# GLL - Lat/Lon data
# GLL - Geographic Latitude and Longitude is a holdover from Loran data and some old units may not send the time and data active information if they are emulating Loran data. If a gps is emulating Loran data they may use the LC Loran prefix instead of GP.
#
#   $GPGLL,4916.45,N,12311.12,W,225444,A,*1D
#
# Where:
#      GLL          Geographic position, Latitude and Longitude
#      4916.46,N    Latitude 49 deg. 16.45 min. North
#      12311.12,W   Longitude 123 deg. 11.12 min. West
#      225444       Fix taken at 22:54:44 UTC
#      A            Data Active or V (void)
#      *iD          checksum data

# $GNGLL,4004.680961,N,11614.576639,E,075414.000,A,A*4F


GLL_INDEX_LATITUDE = 0
GLL_INDEX_LATITUDE_DIRECTION = 1
GLL_INDEX_LONGITUDE = 2
GLL_INDEX_LONGITUDE_DIRECTION = 3
GLL_INDEX_TIME = 4
GLL_INDEX_STATUS = 5

GLL_DATA_LENGTH_MIN = GLL_INDEX_STATUS + 1


class GLL(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

    def decode(self, line):
        result = False

        NmeaSentence.decode(self, line)

        if self.Data is None:
            return result

        if len(self.Data) < GLL_DATA_LENGTH_MIN:
            return result

        self.Latitude = self.Data[GLL_INDEX_LATITUDE]
        self.LatitudeDirection = self.Data[GLL_INDEX_LATITUDE_DIRECTION]
        self.Longitude = self.Data[GLL_INDEX_LONGITUDE]
        self.LongitudeDirection = self.Data[GLL_INDEX_LONGITUDE_DIRECTION]
        self.Time = self.Data[GLL_INDEX_TIME]
        self.Status = self.Data[GLL_INDEX_STATUS]

        self.decode_latitude()
        self.decode_longitude()
        self.decode_time()

        print(self.to_string())

        result = True

        return result

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = NmeaSentence.to_string(self)

        result += self.latitude_to_string() \
                  + self.longitude_to_string() \
                  + self.time_to_string() \
                  + self.status_to_string()

        return result
