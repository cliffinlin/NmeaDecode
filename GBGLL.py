#!/usr/bin/env python
from GLL import GLL


class GBGLL(GLL):
    def __init__(self):
        GLL.__init__(self)

        self.DataType = "$GBGLL"
