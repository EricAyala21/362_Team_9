import datetime
import re
FORMAT_STR = "%Y/%m/%d %H:%M"

def str_to_datetime(s: str):
    """ 
    return a datetime object from the string s with format 'mm/dd/yyyy hr:min'

    Args:
        s (string): string to convert to datetime
    Returns:
        datetime: result datetime object
    """
    return datetime.datetime.strptime(s, FORMAT_STR)


def datetime_to_str(d: datetime.datetime):
    """ 
    return a string from the datetime object d in the format 'mm/dd/yyyy hr:min' 
    
    Args:
        d (datetime): datetime object
    Returns:
        string: fomatted string
    """
    return d.strftime(FORMAT_STR)

def checkDate(date):
    form = re.compile("^[0-9]{4}/[0-1][0-9]/[0-3][0-9]$") #is establishing the xxxx/xx/xx format
    if form.match(date): #checks if the date matches the given format
        return True
    else:
        return False

def checkTime(time):
    form = re.compile("^[0-2][0-9]:[0-6][0-9]$")# is establishing the time format xx:xx
    if form.match(time):
        return True
    else:
        return False
    
def checkTimeInputs(input):
    if isinstance(input,(int,float)): #checks whether the resting time or driving time is a float or a integer 
        return True
    else:
        return False