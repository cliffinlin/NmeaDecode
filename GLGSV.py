#!/usr/bin/env python
from GSV import GSV


class GLGSV(GSV):
    def __init__(self):
        GSV.__init__(self)

        self.DataType = "$GLGSV"
