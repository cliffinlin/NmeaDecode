#!/usr/bin/env python
from GGA import GGA


class GBGGA(GGA):
    def __init__(self):
        GGA.__init__(self)

        self.DataType = "$GBGGA"
