from . import file_manager
from . import log_manager

"""
Subsystem initalisation
Order is of the utmost importance
"""
#Settings
from .ignite_settings import IgniteConfig, CONST_CONFIG_DIR
g_ignite_settings = IgniteConfig()

#threading manager
from .threading_manager import ThreadingManager
g_threading_manager = ThreadingManager(g_ignite_settings)

#costume manager
from .costume_manager import CostumeManager, CONST_SCRIPT_DIR, CONST_COSTUME_DIR
g_costume_manager = CostumeManager()

#pixel manager
from .pixel_strip_manager import PixelStripManager
g_pixel_strip_manager = PixelStripManager()
"""
~subsystem initalisation
"""

def create_file_system():
    file_manager.create_folder(CONST_SCRIPT_DIR)
    file_manager.create_folder(CONST_COSTUME_DIR)
    file_manager.create_folder(CONST_CONFIG_DIR)
    pass

def init_subsystems():
    succes = 1 
    
    g_ignite_settings.import_settings() #load settings
    succes *= g_pixel_strip_manager.initialize_pixel_strip_library()

    if(succes == 0):
        log_manager.error("Error occured while initialising subsystems, app may not work correctly")
    pass


def get_threading_manager():
    return g_threading_manager



create_file_system()
init_subsystems()