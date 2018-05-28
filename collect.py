#!/usr/bin/env python3
from heg.collector import Collector
import sys


if __name__ == '__main__':
    collector = Collector(sys.argv[1:])
    collector.collect()