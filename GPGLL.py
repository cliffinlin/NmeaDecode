#!/usr/bin/env python
from GLL import GLL


class GPGLL(GLL):
    def __init__(self):
        GLL.__init__(self)

        self.DataType = "$GPGLL"
