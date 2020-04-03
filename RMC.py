#!/usr/bin/env python

from NmeaSentence import NmeaSentence

# RMC - recommended minimum data for gps RMC - NMEA has its own version of essential gps pvt (position,
# velocity, time) data. It is called RMC, The Recommended Minimum, which will look similar to: $GPRMC,123519,
# A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
#
# Where:
#      RMC          Recommended Minimum sentence C
#      123519       Fix taken at 12:35:19 UTC
#      A            Status A=active or V=Void.
#      4807.038,N   Latitude 48 deg 07.038' N
#      01131.000,E  Longitude 11 deg 31.000' E
#      022.4        Speed over the ground in knots
#      084.4        Track angle in degrees True
#      230394       Date - 23rd of March 1994
#      003.1,W      Magnetic Variation
#      *6A          The checksum data, always begins with *

# $GNRMC,075414.000,A,4004.680961,N,11614.576639,E,0.031,0.00,240320,,E,A*08

RMC_INDEX_TIME = 0
RMC_INDEX_STATUS = 1
RMC_INDEX_LATITUDE = 2
RMC_INDEX_LATITUDE_DIRECTION = 3
RMC_INDEX_LONGITUDE = 4
RMC_INDEX_LONGITUDE_DIRECTION = 5
RMC_INDEX_SPEED_N = 6
RMC_INDEX_TRACK_ANGLE = 7
RMC_INDEX_DATE = 8

RMC_DATA_LENGTH_MIN = RMC_INDEX_DATE + 1


class RMC(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

        self.TrackAngle = ""

    def decode(self, line):
        NmeaSentence.decode(self, line)

        if self.Data is None:
            return

        if len(self.Data) < RMC_DATA_LENGTH_MIN:
            return

        self.Time = self.Data[RMC_INDEX_TIME]
        self.Status = self.Data[RMC_INDEX_STATUS]
        self.Latitude = self.Data[RMC_INDEX_LATITUDE]
        self.LatitudeDirection = self.Data[RMC_INDEX_LATITUDE_DIRECTION]
        self.Longitude = self.Data[RMC_INDEX_LONGITUDE]
        self.LongitudeDirection = self.Data[RMC_INDEX_LONGITUDE_DIRECTION]
        self.SpeedN = self.Data[RMC_INDEX_SPEED_N]
        self.TrackAngle = self.Data[RMC_INDEX_TRACK_ANGLE]
        self.Date = self.Data[RMC_INDEX_DATE]

        self.decode_time()
        self.decode_latitude()
        self.decode_longitude()
        self.decode_date()

        print(self.to_string())

    def track_angle_to_string(self):
        result = ""

        if len(self.TrackAngle) == 0:
            return result

        result += "TrackAngle="
        result += self.TrackAngle
        result += self.Separate

        return result

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = NmeaSentence.to_string(self)

        result += self.time_to_string() \
                  + self.status_to_string() \
                  + self.latitude_to_string() \
                  + self.longitude_to_string() \
                  + self.speed_n_to_string() \
                  + self.track_angle_to_string() \
                  + self.date_to_string()

        return result
