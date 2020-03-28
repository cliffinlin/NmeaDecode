#!/usr/bin/env python
from RMC import RMC


class BDRMC(RMC):
    def __init__(self):
        RMC.__init__(self)

        self.DataType = "$BDRMC"
