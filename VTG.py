#!/usr/bin/env python

from NmeaSentence import NmeaSentence

# VTG - Vector track an Speed over the Ground VTG - Velocity made good. The gps receiver may use the LC
# prefix instead of GP if it is emulating Loran output. $GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*48
#
# where:
#         VTG          Track made good and ground speed
#         054.7,T      True track made good (degrees)
#         034.4,M      Magnetic track made good
#         005.5,N      Ground speed, knots
#         010.2,K      Ground speed, Kilometers per hour
#         *48          Checksum

# $GNVTG,0.00,T,,M,0.031,N,0.058,K,A*2C

VTG_INDEX_TRUE_TRACK = 0
VTG_INDEX_TRUE_TRACK_MARK = 1
VTG_INDEX_MAGNETIC_TRACK = 2
VTG_INDEX_MAGNETIC_TRACK_MARK = 3
VTG_INDEX_SPEED_N = 4
VTG_INDEX_SPEED_N_MARK = 5
VTG_INDEX_SPEED_M = 6
VTG_INDEX_SPEED_M_MARK = 7

VTG_DATA_LENGTH_MIN = VTG_INDEX_SPEED_M_MARK + 1


class VTG(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

    def decode(self, line):
        NmeaSentence.decode(self, line)

        if self.Data is None:
            return

        if len(self.Data) < VTG_DATA_LENGTH_MIN:
            return

        self.TrueTrack = self.Data[VTG_INDEX_TRUE_TRACK]
        self.TrueTrackMark = self.Data[VTG_INDEX_TRUE_TRACK_MARK]
        self.MagneticTrack = self.Data[VTG_INDEX_MAGNETIC_TRACK]
        self.MagneticTrackMark = self.Data[VTG_INDEX_MAGNETIC_TRACK_MARK]
        self.SpeedN = self.Data[VTG_INDEX_SPEED_N]
        self.SpeedNMark = self.Data[VTG_INDEX_SPEED_N_MARK]
        self.SpeedM = self.Data[VTG_INDEX_SPEED_M]
        self.SpeedMMark = self.Data[VTG_INDEX_SPEED_M_MARK]

        print(self.to_string())

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = NmeaSentence.to_string(self)

        result += self.true_track_to_string() \
                  + self.magnetic_track_to_string() \
                  + self.speed_n_to_string() \
                  + self.speed_m_to_string()

        return result
