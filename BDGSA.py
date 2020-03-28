#!/usr/bin/env python
from GSA import GSA


class BDGSA(GSA):
    def __init__(self):
        GSA.__init__(self)

        self.DataType = "$BDGSA"
