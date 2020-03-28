#!/usr/bin/env python
from GGA import GGA


class GNGGA(GGA):
    def __init__(self):
        GGA.__init__(self)

        self.DataType = "$GNGGA"
