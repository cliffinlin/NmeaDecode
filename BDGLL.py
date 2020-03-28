#!/usr/bin/env python
from GLL import GLL


class BDGLL(GLL):
    def __init__(self):
        GLL.__init__(self)

        self.DataType = "$BDGLL"
