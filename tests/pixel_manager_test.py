import time

from backend import g_pixel_strip_manager as g_pm
from backend import g_costume_manager as g_cm
from backend.costume_manager import Costume, CostumePart, PixelRange
from backend.pixel_strip import TestPixelScript

def test_all():
    test_ws2812xlib()
    return

def test_ws2812xlib():
    sleeptime = 5
    test_range = PixelRange(0, 15)

    pinlist = g_pm.get_initialised_pin_list()
    assert(len(pinlist) == 2)
    
    pixel1 = g_pm.get_neopixel(pinlist[0])
    pixel2 = g_pm.get_neopixel(pinlist[1])
    assert(pixel1 is not None)
    assert(pixel2 is not None)

    pixel1.change_size(16)
    assert(pixel1.get_num_pixels() == 16)

    partled16 = CostumePart(0)
    partled16.name = 'testpart'
    partled16.pixel_ranges.append(test_range)
    partled16.pin = g_pm.get_initialised_pin_list()[0] #pin18

    script = TestPixelScript()
    g_pm.start_script(partled16, script)
    time.sleep(sleeptime)
    assert(not g_pm.start_script(partled16, script))


    assert(g_pm.is_running(partled16))
    g_pm.terminate_script(partled16)
    assert(not g_pm.is_running(partled16))

    # multiple threads and termination test
    amount = 10

    for x in range(amount):
        partledx = CostumePart(x)
        partledx.name = 'testpart_{}'.format(x) 
        partledx.pixel_ranges.append(PixelRange( amount*x, (amount+1)*x -1))
        partledx.pin = g_pm.get_initialised_pin_list()[0] #pin18

        g_pm.start_script(partledx, script)

    assert(len(g_pm.running_costume_parts) == amount)
    g_pm.terminate_all_scripts()
    assert(len(g_pm.running_costume_parts) == 0)
    return