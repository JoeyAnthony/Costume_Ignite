import os, subprocess

from gpiozero import CPUTemperature

"""
Returns a list with all indices from given ranges
multiple_ranges: list of multiple PixelRanges 
"""
def create_element_list(ranges_list):
    EBO = list()
    for el in ranges_list:
        for i in range(el.begin, el.end+1):
            EBO.append(i)
    EBO.sort()
    return EBO

def get_cpu_temp():
    temp = CPUTemperature()
    return temp.temperature

def has_sudo_privilege():
    if os.geteuid() != 0:
        return False
    return True
    
#    ret = 0
#     if os.geteuid() != 0:
#         msg = "[sudo] password for %u:"
#         ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
#     return ret

# class Color:
#     def __init__(self):
#         self.r = 0
#         self.g = 0
#         self.b = 0
        
#     def SetRGBFromWeb(self, rgbstr):
#         translationTable = dict.fromkeys(map(ord, 'rgb()'), None)
#         rgbValues = rgbstr.translate(translationTable)
#         arr = rgbValues.split(',')
        
#         self.r = int(arr[0])
#         self.g = int(arr[1])
#         self.b = int(arr[2])

#     def GetColorArr(self):
#         arr = (self.r, self.g, self.b)
#         return arr

#     def SetRGBFromWeb(self, rgbstr):
#         translationTable = dict.fromkeys(map(ord, 'rgb()'), None)
#         rgbValues = rgbstr.translate(translationTable)
#         arr = rgbValues.split(',')
        
#         self.r = int(arr[0])
#         self.g = int(arr[1])
#         self.b = int(arr[2])

#     def GetColorArr(self):
#         arr = (self.r, self.g, self.b)
#         return arr