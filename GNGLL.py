#!/usr/bin/env python
from GLL import GLL


class GNGLL(GLL):
    def __init__(self):
        GLL.__init__(self)

        self.DataType = "$GNGLL"
