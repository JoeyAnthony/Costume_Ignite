import sys
import linecache

from enum import Enum
from abc import ABC, abstractmethod
from backend import tools
from backend import ignite_settings
from backend import log_manager


class Color:
    def __init__(r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    #parses the rgb string from Wheel Color Picker JQuery plugin
    def ParseWheelColorRGB(self, rgbstr):
        translationTable = dict.fromkeys(map(ord, 'rgb()'), None)
        rgbValues = rgbstr.translate(translationTable)
        arr = rgbValues.split(',')

        self.r = int(arr[0])
        self.g = int(arr[1])
        self.b = int(arr[2])

    #returns colors as an array
    def GetColorArr(self):
        arr = (self.r, self.g, self.b)
        return arr


class IPixelStrip(ABC):

    def __init__(self, pin):
        self.pixel_strip_object = None
        self.GPIOPin = pin

    def get_num_pixels(self):
        return

    def init_pixel_strip(self):
        return

    def deinit_pixel_strip(self):
        return
    
    def change_size(self):
        return
    
    def is_running(self):
        return

    def render(self):
        return

    def render_mutex(self):
        return

    def set_color(self):
        return

    """Returns a list with the pins supported by the library, list should contain integers"""
    def supported_pins(self):
        return


class PixelScript():

    def __init__(self):
        self.printed_no_sudo_warning_once = False

    def start_func(self, pixel_strip:IPixelStrip = None, pixel_ranges = None):
        #Start this function on a TerminationThread
        #Don't override this function
        current_pin = pixel_strip.GPIOPin
        if pixel_strip == None:
            log_manager.warning("Couldn't start script, no neopixel with on pin {} active".format(pin), send_msg=True)
            return
        EBO = tools.create_element_list(pixel_ranges)
        if not tools.has_sudo_privilege() and not self.printed_no_sudo_warning_once:
            log_manager.warning("Running script without sudo privileges")
            self.printed_no_sudo_warning_once = True
        try:
            self._run(pixel_strip, EBO)
        except Exception as e:
            PrintException()
        finally:
            return

    def _run(self, pixel_strip:IPixelStrip, elementList, ar):
        #Override this
        print("Not running script with the right method!")

class TestPixelScript(PixelScript):

    def _run(self, pixel_strip:IPixelStrip, elementList):
        print("Script: %i Start", elementList[0])
        wait = 0.02

        while True:
            # for j in elementList:
            #     pixel_strip[j] = (255//15, 0, 0)
            #     neopixel.Show_ThreadSafe()
            #     time.sleep(wait)

            # for j in elementList:
            #     pixel_strip[j] = (0, 255//15, 0)
            #     pixel_strip.Show_ThreadSafe()
            #     time.sleep(wait)

            # for j in elementList:
            #     pixel_strip[j] = (0, 0, 255//15)
            #     pixel_strip.Show_ThreadSafe()
            #     time.sleep(wait)
            x = wait
        
        print("Script: %i End", elementList[0])


#Function to control leds
def set_color():
    return

def start_script():
    return

def PrintException():
    #Exception information printing
    #https://stackoverflow.com/questions/14519177/python-exception-handling-line-number
    exc_type, exc_obj, tb = sys.exc_info()
    frame = tb.tb_frame
    lineno = tb.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, frame.f_globals)
    log_manager.error("Exception in FILE '{}' LINE: '{}', {}".format(filename, lineno, line.strip()))
    log_manager.error("Exception: {} ".format(exc_obj))
