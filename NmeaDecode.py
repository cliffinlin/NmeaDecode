#!/usr/bin/env python

import os

from BDGGA import BDGGA
from BDGLL import BDGLL
from BDGSA import BDGSA
from BDGSV import BDGSV
from BDRMC import BDRMC
from BDVTG import BDVTG
from GNGGA import GNGGA
from GNGLL import GNGLL
from GNGSA import GNGSA
from GNGSV import GNGSV
from GNRMC import GNRMC
from GNVTG import GNVTG
from GPGGA import GPGGA
from GPGLL import GPGLL
from GPGSA import GPGSA
from GPGSV import GPGSV

# $GNRMC,075414.000,A,4004.680961,N,11614.576639,E,0.031,0.00,240320,,E,A*08
#
# $GNVTG,0.00,T,,M,0.031,N,0.058,K,A*2C
#
# $GNGGA,075414.000,4004.680961,N,11614.576639,E,1,14,0.89,30.372,M,0,M,,*65
#
# $GPGSA,A,3,01,07,08,11,27,28,30,,,,,,1.51,0.89,1.22*05
#
# $BDGSA,A,3,01,03,04,07,08,10,13,,,,,,1.51,0.89,1.22*1C
#
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
#
# $GNGLL,4004.680961,N,11614.576639,E,075414.000,A,A*4F
from GPRMC import GPRMC
from GPVTG import GPVTG


class Nmea:
    def __init__(self):
        self.GPRMC = GPRMC()
        self.BDRMC = BDRMC()
        self.GNRMC = GNRMC()

        self.GPVTG = GPVTG()
        self.BDVTG = BDVTG()
        self.GNVTG = GNVTG()

        self.GPGGA = GPGGA()
        self.BDGGA = BDGGA()
        self.GNGGA = GNGGA()

        self.GPGSA = GPGSA()
        self.BDGSA = BDGSA()
        self.GNGSA = GNGSA()

        self.GPGSV = GPGSV()
        self.BDGSV = BDGSV()
        self.GNGSV = GNGSV()

        self.GPGLL = GPGLL()
        self.BDGLL = BDGLL()
        self.GNGLL = GNGLL()

        self.LastSentence = ""

        self.OutputFile = None

    def set_last_sentence(self, sentence):
        if len(sentence) == 0:
            return

        self.LastSentence = sentence

    def write_to_file(self, text):
        if self.OutputFile is None:
            return

        if len(text) == 0:
            return

        self.OutputFile.write(text + "\n")

    def decode(self):
        input_file_name = "nmea_7537.txt"
        if not os.path.exists(input_file_name):
            print(input_file_name, "file not found!")
            return

        output_file_name = "nmea.out"

        self.OutputFile = open(output_file_name, "w")

        with open(input_file_name) as input_fp:
            for line in input_fp:
                if line is None:
                    continue

                if len(self.LastSentence) > 0 and self.LastSentence in line:
                    continue

                if "$GPRMC" in line:
                    self.GPRMC.decode(line)
                    self.set_last_sentence(self.GPRMC.Sentence)
                    self.write_to_file(self.GPRMC.to_string())
                if "$BDRMC" in line:
                    self.BDRMC.decode(line)
                    self.set_last_sentence(self.BDRMC.Sentence)
                    self.write_to_file(self.BDRMC.to_string())
                if "$GNRMC" in line:
                    self.GNRMC.decode(line)
                    self.set_last_sentence(self.GNRMC.Sentence)
                    self.write_to_file(self.GNRMC.to_string())
                elif "$GPVTG" in line:
                    self.GPVTG.decode(line)
                    self.set_last_sentence(self.GPVTG.Sentence)
                    self.write_to_file(self.GPVTG.to_string())
                elif "$BDVTG" in line:
                    self.BDVTG.decode(line)
                    self.set_last_sentence(self.BDVTG.Sentence)
                    self.write_to_file(self.BDVTG.to_string())
                elif "$GNVTG" in line:
                    self.GNVTG.decode(line)
                    self.set_last_sentence(self.GNVTG.Sentence)
                    self.write_to_file(self.GNVTG.to_string())
                elif "$GPGGA" in line:
                    self.GPGGA.decode(line)
                    self.set_last_sentence(self.GPGGA.Sentence)
                    self.write_to_file(self.GPGGA.to_string())
                elif "$BDGGA" in line:
                    self.BDGGA.decode(line)
                    self.set_last_sentence(self.BDGGA.Sentence)
                    self.write_to_file(self.BDGGA.to_string())
                elif "$GNGGA" in line:
                    self.GNGGA.decode(line)
                    self.set_last_sentence(self.GNGGA.Sentence)
                    self.write_to_file(self.GNGGA.to_string())
                elif "$GPGSA" in line:
                    self.GPGSA.decode(line)
                    self.set_last_sentence(self.GPGSA.Sentence)
                    self.write_to_file(self.GPGSA.to_string())
                elif "$BDGSA" in line:
                    self.BDGSA.decode(line)
                    self.set_last_sentence(self.BDGSA.Sentence)
                    self.write_to_file(self.BDGSA.to_string())
                elif "$GNGSA" in line:
                    self.GNGSA.decode(line)
                    self.set_last_sentence(self.GNGSA.Sentence)
                    self.write_to_file(self.GNGSA.to_string())
                elif "$GPGSV" in line:
                    self.GPGSV.decode(line)
                    self.set_last_sentence(self.GPGSV.Sentence)
                    self.write_to_file(self.GPGSV.to_string())
                elif "$BDGSV" in line:
                    self.BDGSV.decode(line)
                    self.set_last_sentence(self.BDGSV.Sentence)
                    self.write_to_file(self.BDGSV.to_string())
                elif "$GNGSV" in line:
                    self.GNGSV.decode(line)
                    self.set_last_sentence(self.GNGSV.Sentence)
                    self.write_to_file(self.GNGSV.to_string())
                elif "$GPGLL" in line:
                    self.GPGLL.decode(line)
                    self.set_last_sentence(self.GPGLL.Sentence)
                    self.write_to_file(self.GPGLL.to_string())
                elif "$BDGLL" in line:
                    self.BDGLL.decode(line)
                    self.set_last_sentence(self.BDGLL.Sentence)
                    self.write_to_file(self.BDGLL.to_string())
                elif "$GNGLL" in line:
                    self.GNGLL.decode(line)
                    self.set_last_sentence(self.GNGLL.Sentence)
                    self.write_to_file(self.GNGLL.to_string())

        self.OutputFile.close()


def main():
    nmea = Nmea()
    nmea.decode()
    return 0


if __name__ == "__main__":
    main()
