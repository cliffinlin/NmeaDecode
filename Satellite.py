#!/usr/bin/env python

SEPARATE_STRING = " "

SATELLITE_INDEX_PRN = 0
SATELLITE_INDEX_ELEVATION = 1
SATELLITE_INDEX_AZIMUTH = 2
SATELLITE_INDEX_SNR = 3

SATELLITE_DATA_LENGTH_MIN = SATELLITE_INDEX_SNR + 1


class Satellite:
    def __init__(self, data):
        self.Separate = SEPARATE_STRING

        if data is None:
            return

        if len(data) < SATELLITE_DATA_LENGTH_MIN:
            return

        self.PRN = data[SATELLITE_INDEX_PRN]
        self.Elevation = data[SATELLITE_INDEX_ELEVATION]
        self.Azimuth = data[SATELLITE_INDEX_AZIMUTH]
        self.SNR = data[SATELLITE_INDEX_SNR]

    def set(self, prn, elevation, azimuth, snr):
        self.PRN = prn
        self.Elevation = elevation
        self.Azimuth = azimuth
        self.SNR = snr

    def prn_to_string(self):
        result = ""

        if len(self.PRN) == 0:
            return result

        result += "#"
        result += self.PRN
        result += self.Separate

        return result

    def elevation_to_string(self):
        result = ""

        if len(self.Elevation) == 0:
            return result

        result += self.Elevation + "\'"
        result += self.Separate

        return result

    def azimuth_to_string(self):
        result = ""

        if len(self.Azimuth) == 0:
            return result

        result += self.Azimuth + "\'"
        result += self.Separate

        return result

    def snr_to_string(self):
        result = "SNR="

        result += self.SNR
        result += self.Separate
        result += ",\t"

        return result

    def to_string(self):
        result = self.prn_to_string() \
                 + self.elevation_to_string() \
                 + self.azimuth_to_string() \
                 + self.snr_to_string()

        return result
