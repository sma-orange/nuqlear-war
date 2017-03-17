"""utils and helper functions for NuQ"""
import random
import string
import datetime


def pseudo_uid(length=10):
    """make a relatively random 10 character uid from 'english' ascii alphabet and digits 0-9
    :parameter length of returned string, defaults to 10
    :return a pseudo-random string of aA-zZ and 0-9 characters
    """
    rnd = random.SystemRandom()
    alphabet = string.ascii_letters[0:52] + string.digits  # aA-zZ + 0-9
    return str().join(rnd.choice(alphabet) for _ in range(length))


def eta_test(volume=1000, rate=250):
    """estimates time to complete this test with the given parameters
    :parameter volume defaults to 1000
    :parameter rate ~ requests/second
    :return a string as HH:MM:SS
    """
    # TODO: sort out rate & mode -> rate int or whatever
    # TODO: current default to HEAD FAST == 250 r/s ::: fix the table for this matrix
    seconds = volume // rate  # int division
    return datetime.timedelta(seconds=seconds)
