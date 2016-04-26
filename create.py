#!/usr/bin/env python3
"""Create system from kkrtools input file."""
from kkrtools import fileparse
from kkrtools import gencomp


settings = fileparse.get_settings()
gencomp.generate(settings)
