#!/usr/bin/env python3
from heg.collector import Collector
from heg.processor import Processor
import sys


if __name__ == '__main__':
    collector = Collector(sys.argv[1:])
    collector.collect()

    processor = Processor(sys.argv[1:])
    processor.process()