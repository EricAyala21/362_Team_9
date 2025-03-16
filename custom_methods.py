import datetime

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
