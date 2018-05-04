#!/usr/bin/env python3
from heg.collector import Collector
import sys


if __name__ == '__main__':
    app = Collector(sys.argv[1:])
    app.collect()