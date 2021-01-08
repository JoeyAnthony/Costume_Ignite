from backend import file_manager as fm
from backend import log_manager
from backend.database_classes import Costume_DB, CostumePart_DB, CostumePixelStrip_DB
from backend.ignite_settings import CONST_CONFIG_DIR

CONST_COSTUME_DIR = "#costumes"
CONST_SCRIPT_DIR = "#scripts"
CONST_SCRIPTPCKGNM = "scripts"

CONST_PREINIT = 'pre-init'
CONST_MAINSTATE = 'main'
CONST_COSTUME_NAME_PREFIX ='costume_'

"""
Contains a range in a ledstrip from begin to end
"""
class PixelRange:
    def __init__(self, begin=0, end=0):
        #id to the database row
        self.begin = begin
        self.end = end

#CostumeParts have a dict with [presetname][scriptname]
#When turning on a preset
class CostumePreset(object):
    def __init__(self):
        self.presetName = ""

class CostumePart():
    #id = -1 #should never be changed
    pixel_ranges = list() #only the range editor should edit ranges
    name = 'no name'
    pin = -1

    def __init__(self, id):
        self.id = id

    def edit_range(self):
        return

class Costume():
 
    def __init__(self, id=-1):
        self.id = id #Don't edit unless you know what you're doing
        self.pixel_strips = dict() #Don't edit unless you know what you're doing
        self.name = 'no name'
        self.costume_parts = list()

    def save_costume(self):
        if self.id == -1 :
            log_manager.warning("Not saving costume, not initialised")
            return

        jstring = fm.encode_to_json(self)
        fm.write_file(CONST_COSTUME_DIR, CONST_COSTUME_NAME_PREFIX+"{}".format(self.id), jstring)
        log_manager.log("costume save", send_msg=True)
        return

    """
    jsonpickle functions
    """
    def __getstate__(self):
        data = dict()
        data["id"] = self.id
        data["pixel_strips"] = self.pixel_strips
        data["name"] = self.name
        data["costume_parts"] = self.costume_parts
        return data
    def __setstate__(self, state):
        self.id = state["id"]
        self.pixel_strips = state["pixel_strips"]
        self.name = state["name"]
        self.costume_parts = state["costume_parts"]
        pass
    """
    """
        
class CostumeManager():
    __program_state = CONST_PREINIT
    __suit_creation_count = 0
    __current_costume = None
    
    def __init(self):
        return

    def __set_costume(self, costume):
        self.__current_costume = costume

    def get_costumes(self):
        files = fm.get_files_in_folder(CONST_COSTUME_DIR)
        costumes = dict()
        for file in files:
            jstring = fm.open_file(CONST_COSTUME_DIR, file)
            obj = fm.decode_json(jstring)
            if not isinstance(obj, Costume): 
                continue
            costumes[obj.id] = obj.name            
        return costumes

    def load_costume(self, id):
        if not fm.exists(CONST_COSTUME_DIR, id):
            log_manager.error("Couldn't find costume, try again", send_msg=True)
            return

        jstring = fm.open_file(CONST_COSTUME_DIR, id)
        obj = fm.decode_json(jstring)
        if (obj is None):
            log_manager.error("Couldn't load costume, try again", send_msg=True)
            return
        
        self.__current_costume = obj
        log_manager.log("Costume loaded", send_msg=True)
        return

    def create_and_save_new_costume(self, name=None):
        files = fm.get_files_in_folder(CONST_COSTUME_DIR)
        # if no files exist
        if len(files) == 0:
            cos = Costume(0)
            if name is not None:
                cos.name = name
            else:
                cos.name +=("_" + 0)
            cos.save_costume()
            return cos

        #they exist
        nums = list()
        for file in files:
            try:
                nums.append(int(file.replace(CONST_COSTUME_NAME_PREFIX, '')))
            except:
                log_manager.error("File found with no integer as id! {}".format(file))
                continue
        
        highest = 0
        if len(nums) is not 0:
            highest += max(nums)+1

        cos = Costume(highest)
        if name is not None:
            cos.name = name
        else:
            cos.name +=("_" + highest)
        cos.save_costume()
        return cos

    def delete_costume(self, id):
        if fm.exists(CONST_COSTUME_DIR, CONST_COSTUME_NAME_PREFIX+'{}'.format(id)):
            fm.delete_file(CONST_COSTUME_DIR, CONST_COSTUME_NAME_PREFIX+'{}'.format(id))
            log_manager.log("Costume deleted", send_msg=True)
        else:
            log_manager.log("Costume not found")
        return
    
    #Returns costume if in the correct state, None otherwise
    def get_costume(self):
        if self.__program_state == CONST_MAINSTATE :
            return self.__current_costume
        else:
            return None

    def get_program_state(self):
        return self.__program_state
