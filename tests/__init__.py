#custom imports
from tests import rpi_ws281x_pixelstrip_test
from tests import threading_test
from tests import costume_manager_test
from tests import pixel_manager_test

def RunAllTests():
    #costume_manager_test.TestAll()
    rpi_ws281x_pixelstrip_test.TestAll() #only works with sudo
    #threading_test.Test_All()
    #pixel_manager_test.test_all()