#!/usr/bin/env python
from GGA import GGA


class BDGGA(GGA):
    def __init__(self):
        GGA.__init__(self)

        self.DataType = "$BDGGA"
