from backend.rpi_ws281xlib.rpi_ws281x_pixelstrip import rpi_ws281x_PixelStrip
#from backend import pixel_strip
import time

def endless_test():
    numpix = 50
    tpin = 18
    sleep_time = 200/1000.0

    strip = rpi_ws281x_PixelStrip(numpix, tpin, brightness= 100)
    strip.init_pixel_strip()

    strip.make_one_color(150, 95 , 10)

    while True:
        for i in range(numpix):
            strip.set_color(i, 200, 0, 55)
            strip.render()
            time.sleep(sleep_time)

        for i in range(numpix):
            strip.set_color(i, 100, 155, 0)
            strip.render()
            time.sleep(sleep_time)

        for i in range(numpix):
            strip.set_color(i, 155, 0, 100)
            strip.render()
            time.sleep(sleep_time)

