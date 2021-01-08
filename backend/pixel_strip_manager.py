from enum import Enum
from backend import log_manager
from .rpi_ws281xlib import rpi_ws281x_pixelstrip as rpi_ws28x
from backend import tools
from backend.costume_manager import Costume, CostumePart, PixelRange
from backend.pixel_strip import PixelScript
from backend.threading_manager import TerminationThread

from backend import g_threading_manager as g_tm

CONST_INIT_BRIGHTNESS = 255
CONST_INIT_LEDCOUNT = 10

PIN_D18 = 18 #PWM0
PIN_D13 = 13 #PWM1
PIN_D21 = 21 #PCM
PIN_D10 = 10 #SPI

class LibraryTypes(Enum):
    WS2812 = 0
    ADAFRUIT = 1
CONST_DEFAULT_LIBRARY = LibraryTypes.WS2812

# class ProcessID:
#     def __init__(self):
#         self.process = None
#         self.partname = ""
#         pass
#     pass

def __init_Adafruit():
    return

def init_rpi_ws281x():
    strips = dict()
    strips[rpi_ws28x.CONST_D18] = rpi_ws28x.rpi_ws281x_PixelStrip(rpi_ws28x.CONST_INITIAL_LED_COUNT, rpi_ws28x.CONST_D18, brightness=CONST_INIT_BRIGHTNESS)
    strips[rpi_ws28x.CONST_D13] = rpi_ws28x.rpi_ws281x_PixelStrip(rpi_ws28x.CONST_INITIAL_LED_COUNT, rpi_ws28x.CONST_D13, brightness=CONST_INIT_BRIGHTNESS)
    return strips

class PixelStripManager:
    def __init__(self):
        self.__initialised = False
        self.initialised_pixel_strips = dict() #[pin number] = PixelStrip
        self.running_costume_parts = dict() #[costume_part id] = thread_id
        return

    def initialize_pixel_strip_library(self):
        #initialize strips on all pins
        #take led library as argument to init
        if self.__initialised:
            return True

        from backend import g_ignite_settings as g_is

        if(g_is.active_library == None):
            log_manager.error("No Library selected, using default")
            g_is.active_library = CONST_DEFAULT_LIBRARY

        if(g_is.active_library == LibraryTypes.WS2812):
            self.initialised_pixel_strips = init_rpi_ws281x()
            self.__initialised = True
            return True
            
        elif(g_is.active_library == LibraryTypes.ADAFRUIT):
            self.__initialised = True
            return True
        return False

    def get_initialised_pin_list(self):
        if not self.__initialised or len(self.initialised_pixel_strips) == 0:
            return None
        return rpi_ws28x.rpi_ws281x_PixelStrip.supported_pins()

    def get_neopixel(self, pin):
        if pin not in self.initialised_pixel_strips.keys():
            return None
        return self.initialised_pixel_strips[pin]

    def start_script(self, costume_part:CostumePart, pixel_script:PixelScript):
        if not self.__initialised:
            return None

        ranges = costume_part.pixel_ranges
        neopixel = self.get_neopixel(costume_part.pin)
        if costume_part.id in self.running_costume_parts:
            log_manager.warning("Costume part is already active {} active".format(costume_part.name), send_msg=True)
            return False
        if neopixel == None:
            log_manager.warning("Couldn't start script, no neopixel with on pin {} active".format(costume_part.pin), send_msg=True)
            return False

        thread = TerminationThread(name=costume_part.id, target=pixel_script.start_func, args=(neopixel, ranges))

        self.running_costume_parts[costume_part.id] = g_tm.add_termination_thread(thread)
        thread.start()
        return True

    def terminate_script(self, costume_part:CostumePart):
        if not self.__initialised:
            return None
        thread_id = self.running_costume_parts[costume_part.id]
        if g_tm.terminate_thread(thread_id):
            self.running_costume_parts.pop(costume_part.id)
            log_manager.log("script stopped", send_msg=True)
        else:
            log_manager.error("An error occurred, couldn't stop script. If the program behaves in unexpected ways please restart", send_msg=True)
        return

    def terminate_all_scripts(self):
        if not self.__initialised:
            return None

        terminated_thread_ids = list()
        if g_tm.terminate_all_termination_tasks(terminated_thread_ids):
            log_manager.log("scripts stopped", send_msg=True)
            #self.__cleanup_active_costume_parts()
        else:
            log_manager.error("couldn't stop all scripts, please restart program", send_msg=True)

        # remove terminated threads from running_costume_parts
        running_parts = {key:val for key, val in self.running_costume_parts.items() if val not in terminated_thread_ids}
        self.running_costume_parts = running_parts
        return

    def is_running(self, costume_part: CostumePart):
        if not self.__initialised:
            return None

        if costume_part.id in self.running_costume_parts.keys():
            return True
        return False
    
    def __cleanup_active_costume_parts(self):
        indices = list()
        #get info from threadmanager and decide if thread is running or not
        #or maybe that's not necessary, check script termination functions
        for part_id in self.running_costume_parts:
            thread_id = self.running_costume_parts[part_id]
            thread = g_tm.get_termination_thread(thread_id)
            if thread == None or not thread.is_alive():
                indices.append(part)
                continue

        for index in indices:
            self.running_costume_parts.pop(index)
