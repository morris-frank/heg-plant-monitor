import datetime
import re
import sys
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


def query_boolean(question, default='yes', defaulting=False):
    """[summary]
    
    Arguments:
        question {str} -- THe string to present to the user
    
    Keyword Arguments:
        default {str} -- The default answer (default: {'yes'})
        defaulting {bool} -- If true just pass along the default answer (default: {False})
    
    Returns:
        bool -- THY ANTWOORD
    """
    valid = {'yes': True, 'y': True, 'ye': True, 'j': True, 'ja': True,
             'no': False, 'n': False, 'nein': False}
    if defaulting:
        return valid[default]
    if default is None:
        prompt = ' (y/n) '
    elif default == 'yes':
        prompt = ' ([Y]/n) '
    elif default == 'no':
        prompt = ' (y/[N]) '
    else:
        raise ValueError('invalid default answer: {}'.format(default))
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            print(default)
            return valid[default]
        elif choice in valid:
            print(choice)
            return valid[choice]
        else:
            print('Please respond with "yes" or "no" '
                  '(or "y" or "n").')
