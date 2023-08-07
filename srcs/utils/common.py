import re

def first_int(txt):
    """returns int, if none, None"""
    no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", txt)
    if no:
        return int(no[0])
    return None

def first_float(txt):
    """returns int, if none, None"""
    no = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[.]?\d*(?:[eE][-+]?\d+)?", txt)
    if no:
        return float(no[0])
    return None

def reduceLineBreak(the_string: str):
    """returns string with 1 linebreak and stripped"""
    the_string = the_string.strip()
    while "\n\n" in the_string:
        the_string = the_string.replace("\n\n", "\n")
    return the_string