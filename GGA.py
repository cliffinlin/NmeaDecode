#!/usr/bin/env python

from NmeaSentence import NmeaSentence

# GGA - Fix information
# GGA - essential fix data which provide 3D location and accuracy data.
#  $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
#
# Where:
#      GGA          Global Positioning System Fix Data
#      123519       Fix taken at 12:35:19 UTC
#      4807.038,N   Latitude 48 deg 07.038' N
#      01131.000,E  Longitude 11 deg 31.000' E
#      1            Fix quality: 0 = invalid
#                                1 = GPS fix (SPS)
#                                2 = DGPS fix
#                                3 = PPS fix
# 			       4 = Real Time Kinematic
# 			       5 = Float RTK
#                  6 = estimated (dead reckoning) (2.3 feature)
# 			       7 = Manual input mode
# 			       8 = Simulation mode
#      08           Number of satellites being tracked
#      0.9          Horizontal dilution of position
#      545.4,M      Altitude, Meters, above mean sea level
#      46.9,M       Height of geoid (mean sea level) above WGS84
#                       ellipsoid
#      (empty field) time in seconds since last DGPS update
#      (empty field) DGPS station ID number
#      *47          the checksum data, always begins with *

# $GNGGA,075414.000,4004.680961,N,11614.576639,E,1,14,0.89,30.372,M,0,M,,*65

GGA_INDEX_TIME = 0
GGA_INDEX_LATITUDE = 1
GGA_INDEX_LATITUDE_DIRECTION = 2
GGA_INDEX_LONGITUDE = 3
GGA_INDEX_LONGITUDE_DIRECTION = 4
GGA_INDEX_FIX_QUALITY = 5
GGA_INDEX_TRACKED_NUMBER = 6
GGA_INDEX_HDOP = 7
GGA_INDEX_ALTITUDE = 8
GGA_INDEX_ALTITUDE_UNIT = 9
GGA_INDEX_GEOID_SEPARATION = 10
GGA_INDEX_GEOID_SEPARATION_UNIT = 11
GGA_INDEX_DIFFERENTIAL_DATA_AGE = 12
GGA_INDEX_REFERENCE_STATION_ID = 13

GGA_DATA_LENGTH_MIN = GGA_INDEX_REFERENCE_STATION_ID + 1


class GGA(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

    def decode(self, line):
        NmeaSentence.decode(self, line)

        if self.Data is None:
            return

        if len(self.Data) < GGA_DATA_LENGTH_MIN:
            return

        self.Time = self.Data[GGA_INDEX_TIME]
        self.Latitude = self.Data[GGA_INDEX_LATITUDE]
        self.LatitudeDirection = self.Data[GGA_INDEX_LATITUDE_DIRECTION]
        self.Longitude = self.Data[GGA_INDEX_LONGITUDE]
        self.LongitudeDirection = self.Data[GGA_INDEX_LONGITUDE_DIRECTION]
        self.FixQuality = self.Data[GGA_INDEX_FIX_QUALITY]
        self.TrackedNumber = self.Data[GGA_INDEX_TRACKED_NUMBER]
        self.HDOP = self.Data[GGA_INDEX_HDOP]
        self.Altitude = self.Data[GGA_INDEX_ALTITUDE]
        self.AltitudeUnit = self.Data[GGA_INDEX_ALTITUDE_UNIT]
        self.GeoidSeparation = self.Data[GGA_INDEX_GEOID_SEPARATION]
        self.GeoidSeparationUnit = self.Data[GGA_INDEX_GEOID_SEPARATION_UNIT]
        self.DifferentialDataAge = self.Data[GGA_INDEX_DIFFERENTIAL_DATA_AGE]
        self.ReferenceStationID = self.Data[GGA_INDEX_REFERENCE_STATION_ID]

        self.decode_time()
        self.decode_latitude()
        self.decode_longitude()

        print(self.to_string())

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = NmeaSentence.to_string(self)

        result += self.time_to_string() \
                  + self.latitude_to_string() \
                  + self.longitude_to_string() \
                  + self.fix_quality_to_string() \
                  + self.tracked_number_to_string() \
                  + self.hdop_to_string() \
                  + self.altitude_to_string() \
                  + self.geoid_separation_to_string() \
                  + self.differential_data_age_to_string()\
                  + self.reference_station_id_to_string()

        return result
