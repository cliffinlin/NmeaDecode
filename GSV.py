#!/usr/bin/env python

from NmeaSentence import NmeaSentence
from Satellite import Satellite

# GSV - Detailed Satellite data
# GSV - Satellites in View shows data about the satellites that the unit might be able to find based on its viewing mask and almanac data. It also shows current ability to track this data. Note that one GSV sentence only can provide data for up to 4 satellites and thus there may need to be 3 sentences for the full information. It is reasonable for the GSV sentence to contain more satellites than GGA might indicate since GSV may include satellites that are not used as part of the solution. It is not a requirment that the GSV sentences all appear in sequence. To avoid overloading the data bandwidth some receivers may place the various sentences in totally different samples since each sentence identifies which one it is.
# The field called SNR (Signal to Noise Ratio) in the NMEA standard is often referred to as signal strength. SNR is an indirect but more useful value that raw signal strength. It can range from 0 to 99 and has units of dB according to the NMEA standard, but the various manufacturers send different ranges of numbers with different starting numbers so the values themselves cannot necessarily be used to evaluate different units. The range of working values in a given gps will usually show a difference of about 25 to 35 between the lowest and highest values, however 0 is a special case and may be shown on satellites that are in view but not being tracked.
#   $GPGSV,2,1,08,01,40,083,46,02,17,308,41,12,07,344,39,14,22,228,45*75
#
# Where:
#       GSV          Satellites in view
#       2            Number of sentences for full data
#       1            sentence 1 of 2
#       08           Number of satellites in view
#
#       01           Satellite PRN number
#       40           Elevation, degrees
#       083          Azimuth, degrees
#       46           SNR - higher is better
#            for up to 4 satellites per sentence
#       *75          the checksum data, always begins with *

# $GPGSV,3,1,09,01,45,166,44,07,64,246,46,08,55,042,45,11,77,113,43*7F
#
# $GPGSV,3,2,09,20,,,22,22,,,21,27,23,055,26,28,18,296,36*7B
#
# $GPGSV,3,3,09,30,44,299,43*46
#
# $BDGSV,3,1,10,01,38,144,39,02,31,223,00,03,43,188,41,04,26,123,39*63
#
# $BDGSV,3,2,10,05,14,246,00,07,76,070,41,08,42,172,40,09,10,210,00*69
#
# $BDGSV,3,3,10,10,71,319,41,13,21,189,41*64

GSV_SATELLITE_DATA_LENGTH = 4
GSV_SATELLITE_COUNT_MAX = 4

GSV_INDEX_TOTAL = 0
GSV_INDEX_CURRENT = 1
GSV_INDEX_VIEW = 2

GSV_DATA_LENGTH_MIN = GSV_INDEX_VIEW + 1


class GSV(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

        self.Total = ""
        self.Current = ""
        self.SignalId = ""

    def decode(self, line):
        result = False

        NmeaSentence.decode(self, line)

        if self.Data is None:
            return result

        if len(self.Data) < GSV_DATA_LENGTH_MIN:
            return result

        self.Total = self.Data[GSV_INDEX_TOTAL]
        self.Current = self.Data[GSV_INDEX_CURRENT]
        self.View = self.Data[GSV_INDEX_VIEW]

        self.SatelliteList = []

        index = GSV_INDEX_VIEW + 1
        count = int((len(self.Data) - GSV_DATA_LENGTH_MIN) / 4)

        for i in range(0, count):
            data = self.Data[index:index + GSV_SATELLITE_DATA_LENGTH]
            self.SatelliteList.append(Satellite(data))
            index += GSV_SATELLITE_DATA_LENGTH

        if ((len(self.Data) + 1) % GSV_SATELLITE_DATA_LENGTH) == 1:
            self.SignalId = self.Data[len(self.Data) - 1]

        print(self.to_string())

        result = True

        return result

    def current_total_to_string(self):
        result = ""

        if len(self.Current) == 0 or len(self.Total) == 0:
            return result

        result += self.Current + "/" + self.Total
        result += self.Separate

        return result

    def signal_id_to_string(self):
        result = ""

        if len(self.SignalId) == 0:
            return result

        result += "SignalId="
        result += self.SignalId
        result += self.Separate

        return result

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = NmeaSentence.to_string(self)

        result += self.current_total_to_string() \
                  + self.view_to_string() \
                  + self.satellite_list_to_string() \
                  + self.signal_id_to_string()

        return result
