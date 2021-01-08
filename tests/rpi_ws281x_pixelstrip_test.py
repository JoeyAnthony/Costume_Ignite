from backend.rpi_ws281xlib.rpi_ws281x_pixelstrip import rpi_ws281x_PixelStrip
#from backend import pixel_strip
import time

def TestAll():
    #piano()
    single_strip()
    #multi_strip()

def piano():
    numpix = 16
    tpin = 18

    strip = rpi_ws281x_PixelStrip(numpix, tpin, brightness= 10)
    strip.init_pixel_strip()

    strip.make_one_color( 48,255, 75)
    strip.render()

def Test_ws281x_PixelStripClass():
    
    return

def single_strip():
    numpix = 16
    tpin = 18
    sleep_time = 20/1000.0

    strip = rpi_ws281x_PixelStrip(numpix, tpin, brightness= 20)
    strip.init_pixel_strip()

    assert strip.get_num_pixels() == numpix
    strip.make_one_color(255, 0 , 0)
    strip.render()

    for i in range(numpix):
        strip.set_color(i, 0, 0, 255)
        strip.render()
        time.sleep(sleep_time)

    strip.make_one_color(0, 0, 0)

    numpix = 48
    strip.change_size(numpix)

    print("NUMBERPIX = %i", strip.get_num_pixels())
    assert strip.get_num_pixels() == numpix

    for i in range(strip.get_num_pixels()):
        strip.set_color(i, 255, 0, 0)
        strip.render()
        time.sleep(sleep_time)

    for i in range(strip.get_num_pixels()):
        strip.set_color(i, 0, 255, 0)
        strip.render()
        time.sleep(sleep_time)

    for i in range(strip.get_num_pixels()):
        strip.set_color(i, 0, 0, 255)
        strip.render()
        time.sleep(sleep_time)

    strip.make_one_color(0, 0, 0)
    strip.deinit_pixel_strip()


def multi_strip():
    numpix = 150
    pin1 = 18
    pin2 = 13
    dma1 = 10
    dma2 = 11
    channel1 = 0
    channel2 = 1
    sleep_time = 0.1

    strip1 = rpi_ws281x_PixelStrip(numpix, pin1, brightness= 20, dma=dma1, channel=channel1)
    strip1.init_pixel_strip()

    strip2 = rpi_ws281x_PixelStrip(numpix, pin2, brightness= 20, dma=dma1, channel=channel2)
    strip2.init_pixel_strip()

    for i in range(numpix):
        strip1.set_color(i, 255, 0, 0)     
        strip2.set_color(i, 0, 255, 0)
        strip1.render()
        strip2.render()
        time.sleep(sleep_time)
