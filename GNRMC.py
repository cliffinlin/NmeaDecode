#!/usr/bin/env python
from RMC import RMC


class GNRMC(RMC):
    def __init__(self):
        RMC.__init__(self)

        self.DataType = "$GNRMC"
