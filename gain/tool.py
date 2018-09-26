import re
import logging
from typing import List

# Becomes clean and accepts str, list, dict
def clean(s:(str, list)) -> (str, list) or None:
    """
        s = string to clean
        Clean tabs, spaces, newlines and unwanted Unicode characters
        Returns cleaned string
    """
    def _clean(s:str) -> str or None:
        # Tuples can contain any method and argument length that you need to clean the string
        default_actions = (
            ('replace', '\n', ' '),
            ('replace', '\t', ' '),
            ('replace', '\r', ' '),
            ('strip',)
            )
        for method in default_actions:
            args = tuple(list(method)[1::])
            s = s.__getattribute__(list(method)[0])(*args)
        s = ' '.join(s.split())
        return s
    
    if isinstance(s, str):
        return _clean(s)

    elif isinstance(s, list):
        return [_clean(item) for item in s]

def clean_numeric(s:str) -> str or s:
    """s = '3.55,-'; clean_numeric(s)
    >>> 3.55
    s = '1.5600,55' <-- Metric system
    >>> 15600.55
    """
    if s:
        s = str_num_only(s.replace(',', '.'), protect_char='.')
        if s.count('.') >= 2:
            n = s.rsplit('.', 1)
            s = ''.join(n[0:len(n)-1]).replace('.', '') + '.' + s.rsplit('.', 1)[-1]
        return s
    else:
        return s


def str_num_only(s, protect_char='') -> str or s:
    """ s = "$%^&123!#!$"; str_num_only(s)
    >>> 123
    s = "$%^&123!#!$"; str_num_only(s, protect_char="$")
    >>> $123$
    """
    if isinstance(s, str):
        return ''.join(filter(lambda x: x.isdigit() or x == protect_char, s))
    else:
        return s

# Separate code
# Users should decide on this, not me
def clean_phone_number(s:str) -> str:
    """s = "+ 32 16 23 69 36"
    clean_phone_number(s)
    >>> 003212236936
    # + is being replaced by '00'
    # if len(s) < 8, string becomes None"""

    if s:
        s = s.replace('+', '00')
        s = str_num_only(s)
        return s
    else:
        return s

# Remove clean phone number
# Users can apply clean to gain the same affect.
def extract_phone(s:str) -> list:
    """ s = 'Company Name and Email: info@example-travel.com Tel.: 025 - 5339007 Mob.: +316-11465330,tel is 0031-6190-60870 and 06 31 28 08 74 or 06 1802 0872'
    extract_phone(s)
    >>> ['0255339007', '0031611465330', '0031619060870', '0631280874', '0618020872']
    """
    regex = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    s = re.findall(regex, s)

    phone_list = []
    for phone in s:
        phone = clean_phone_number(phone)
        if phone:
            phone_list.append(phone)

    return phone_list


def extract_email(s:str) -> list:
    return re.findall(r'[\w\.-]+@[\w\.-]+', s)


def extract_website(s:str) -> list:
    return re.findall(r'https?://|www(?:[-\w.]|(?:%[\da-fA-F]{2}))+', s)


def unique_list(l:list) -> List[str or int]:
    """Remove duplicates from list, while maintaining order
    >>> unique([3,6,4,4,6])
    [3, 6, 4]"""
    checked = []
    for e in l:
        if e not in checked:
            checked.append(e)
    return checked


def to_date_iso(datestring: str) -> str:
    """
    Takes a string of a human-readable date and
    returns a machine-readable date string.

    >>> date_to_iso('20 July 2002')
    '2002-07-20 00:00:00'
    >>> date_to_iso('June 3 2009 at 4am')
    '2009-06-03 04:00:00'
    """
    # todo: remove the python-dateutil dependency or
    # make it a choice to the user
    from dateutil import parser
    from datetime import datetime
    default = datetime(year=1, month=1, day=1)
    return str(parser.parse(datestring, default=default))


class Manipulation:
    @staticmethod
    def clean(s):
        return clean(s)

    @staticmethod
    def str_num_only(s):
        return str_num_only(s, protect_char='')

    @staticmethod
    def clean_numeric(s):
        return clean_numeric(s)

    @staticmethod
    def clean_phone_number(s):
        return clean_phone_number(s)

    @staticmethod
    def extract_phone(s):
        return extract_phone(s)

    @staticmethod
    def extract_email(s):
        return extract_email(s)

    @staticmethod
    def unique_list(l):
        return unique_list(l)

    @staticmethod
    def extract_website(s):
        return extract_website(s)

    @staticmethod
    def to_date_iso(s):
        return to_date_iso(s)
