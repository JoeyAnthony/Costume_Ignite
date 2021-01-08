from backend import log_manager
from backend import file_manager as fm
from backend import tools

CONST_CONFIG_DIR = "#config"
CONST_CONFIG_FILENAME = "Config.json"
CONST_CONFIG_MAX_DEFAULT_THREAD_COUNT = 15
CONST_CONFIG_ID = "IgniteConfigID"

class IgniteConfig():
    def __init__(self):
        self.active_library = None
        self.max_thread_count = CONST_CONFIG_MAX_DEFAULT_THREAD_COUNT
        self.has_sudo_privileges = tools.has_sudo_privilege()
        pass

    """
    jsonpickle functions
    """
    def __getstate__(self):
        data = dict()
        data["lib"] = self.active_library
        return data
    def __setstate__(self, state):
        self.active_library = state["lib"]
        pass
    """
    """

    def save_settings(self):
        jstring = fm.encode_to_json(self)
        fm.write_file(CONST_CONFIG_DIR, CONST_CONFIG_FILENAME, jstring)
        pass

    #load saved settings
    def import_settings(self):
        jstring = fm.open_file(CONST_CONFIG_DIR, CONST_CONFIG_FILENAME)
        load = fm.decode_json(jstring)
        if not load:
            self.save_settings()
            log_manager.log("Created settings file")
            return True

        if(load.active_library == ""):
            log_manager.error("Couldn't import ignite configs, setting defaults")
            
            return False

        log_manager.log("Ignite configs imported")
        return True
    