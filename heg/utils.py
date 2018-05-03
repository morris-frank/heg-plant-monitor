import datetime
import unicodedata
import re

class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


def daterange(start_date, stop_date):
    assert(isinstance(start_date, datetime.date))
    assert(isinstance(stop_date, datetime.date))
    for n in range(int((stop_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)