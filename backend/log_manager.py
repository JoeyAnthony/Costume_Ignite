import warnings
from datetime import datetime

def log(*args, send_msg = False):
    print(bcolors.OKBLUE + ''.join(map(str, args)) + __get_current_time_string() + bcolors.ENDC)
    if(send_msg):
        testlog("SEND")

def warning(*args, send_msg = False):
    print(bcolors.WARNING + ''.join(map(str, args))+ __get_current_time_string() + bcolors.ENDC)
    pass

def error(*args, send_msg = False):
    print(bcolors.FAIL + ''.join(map(str, args))+ __get_current_time_string() + bcolors.ENDC)
    pass

def testlog(*args):
    print(bcolors.HEADER + ''.join(map(str, args))+ __get_current_time_string() + bcolors.ENDC)
    pass

def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)

def __get_current_time_string():
    return "\t" + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


#TODO add time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
