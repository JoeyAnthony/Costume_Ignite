import threading

import rpi_ws281x

from backend.pixel_strip import IPixelStrip, Color
from backend import g_ignite_settings as g_is

CONST_D18 = 18
CONST_D13 = 13
CONST_INITIAL_LED_COUNT = 10


class rpi_ws281x_PixelStrip(IPixelStrip):
    def __init__(self, num, pin, dma=10, brightness=255, channel=0):
        super().__init__(pin)
        self.ws281x = rpi_ws281x.PixelStrip(num, pin, dma=dma, brightness=brightness, channel=channel)
        self.bck_dma = dma
        self.bck_brightness = brightness
        self.bck_channel = channel
        self.thread_lock = threading.Lock()
        
    def __getitem__(self, idx):
        return self.ws281x.getPixelColor(idx)

    def supported_pins():
        return [CONST_D18, CONST_D13]

    def get_num_pixels(self):
        return self.ws281x.numPixels()

    def init_pixel_strip(self):
        self.ws281x.begin()
        pass

    def deinit_pixel_strip(self):
        self.ws281x._cleanup()
        pass
    
    def change_size(self, num):
        #rpi_ws281x.ws.ws2811_channel_t_count_set(self.ws281x._channel, num)
        self.ws281x._cleanup()
        self.__init__(num, self.GPIOPin, self.bck_dma, self.bck_brightness, self.bck_channel)
        self.init_pixel_strip()
        pass

    def render(self):
        self.thread_lock.acquire()
        if g_is.has_sudo_privileges:
            self.ws281x.show()
        self.thread_lock.release()
        pass

    def _render_no_lock(self):
        if g_is.has_sudo_privileges:
            self.ws281x.show()
        pass

    def make_one_color(self, r, g, b):
        for i in range(self.ws281x.numPixels()):
            self.ws281x.setPixelColorRGB(i, r, g, b)
        pass

    def set_color(self, n, r, g, b):
        self.ws281x.setPixelColorRGB(n, r, g, b)

    # def set_color(self, n, color:Color):
    #     self.ws281x.setPixelColorRGB(n, color.r, color.g, color.blueb)


        