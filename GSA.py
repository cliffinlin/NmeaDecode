#!/usr/bin/env python

from NmeaSentence import NmeaSentence

# GSA - Overall Satellite data GSA - GPS DOP and active satellites. This sentence provides details on the
# nature of the fix. It includes the numbers of the satellites being used in the current solution and the
# DOP. DOP (dilution of precision) is an indication of the effect of satellite geometry on the accuracy of
# the fix. It is a unitless number where smaller is better. For 3D fixes using 4 satellites a 1.0 would be
# considered to be a perfect number, however for overdetermined solutions it is possible to see numbers below
# 1.0. $GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39
#
# Where:
#      GSA      Satellite status
#      A        Auto selection of 2D or 3D fix (M = manual)
#      3        3D fix - values include: 1 = no fix
#                                        2 = 2D fix
#                                        3 = 3D fix
#      04,05... PRNs of satellites used for fix (space for 12)
#      2.5      PDOP (dilution of precision)
#      1.3      Horizontal dilution of precision (HDOP)
#      2.1      Vertical dilution of precision (VDOP)
#      *39      the checksum data, always begins with *

# $GPGSA,A,3,01,07,08,11,27,28,30,,,,,,1.51,0.89,1.22*05

# $BDGSA,A,3,01,03,04,07,08,10,13,,,,,,1.51,0.89,1.22*1C


GSA_INDEX_SELECTION = 0
GSA_INDEX_FIX_TYPE = 1
GSA_INDEX_USED_MIN = 2
GSA_INDEX_USED_MAX = 13
GSA_INDEX_PDOP = 14
GSA_INDEX_HDOP = 15
GSA_INDEX_VDOP = 16

GSA_DATA_LENGTH_MIN = GSA_INDEX_VDOP + 1


class GSA(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

    def decode(self, line):
        NmeaSentence.decode(self, line)

        if self.Data is None:
            return

        if len(self.Data) < GSA_DATA_LENGTH_MIN:
            return

        self.Selection = self.Data[GSA_INDEX_SELECTION]
        self.FixType = self.Data[GSA_INDEX_FIX_TYPE]
        self.Used = self.Data[GSA_INDEX_USED_MIN:GSA_INDEX_USED_MAX]
        self.PDOP = self.Data[GSA_INDEX_PDOP]
        self.HDOP = self.Data[GSA_INDEX_HDOP]
        self.VDOP = self.Data[GSA_INDEX_VDOP]

        print(self.to_string())

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = NmeaSentence.to_string(self)

        result += self.selection_to_string() \
                  + self.fix_type_to_string() \
                  + self.used_to_string() \
                  + self.pdop_to_string() \
                  + self.hdop_to_string() \
                  + self.vdop_to_string()

        return result
