#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) >= 2:
    filename = sys.argv[1]
else:
    filename = "./examples.print8.ls8"

cpu = CPU()

cpu.load(filename)
cpu.run()