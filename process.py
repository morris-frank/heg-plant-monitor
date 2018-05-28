#!/usr/bin/env python3
from heg.processor import Processor
import sys


if __name__ == '__main__':
    processor = Processor(sys.argv[1:])
    processor.process()