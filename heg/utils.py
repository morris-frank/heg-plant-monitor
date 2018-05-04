import datetime
import re
import unicodedata


def daterange(start_date, stop_date):
    """Generator function for a range of dates.
    
    Arguments:
        start_date {datetime.date} -- The date to start with
        stop_date {datetime.date} -- The date to stop at
    """
    assert(isinstance(start_date, datetime.date))
    assert(isinstance(stop_date, datetime.date))
    for n in range(int((stop_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def slugify(value):
    """_Slugifies_ a given string. Meaning it makes it a good URI or Filename slug/part.
    
    Arguments:
        value {string} -- The string to process
    
    Returns:
        string -- The processed string
    """
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)
