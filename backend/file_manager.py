import os
import jsonpickle as json
import importlib
from . import log_manager

def get_files_in_folder(path):
    try:
        return os.listdir(path)
    except:
        log_manager.warning("Could not get a list of dirs")    
        return []

def create_folder(path):
    if os.path.exists(path):
        log_manager.log("Directory already exists")
        return
        
    try:
        os.makedirs(path)
    except:
        log_manager.warning("Could not create dir")
    else:
        log_manager.log("Created folder structure: ", path)

def delete_folder(path):
    try:
        os.rmdir(path)
    except:
        log_manager.warning("Could not delete dir")
    else:
        log_manager.log("Deleted folder structure: ", path)

def encode_to_json(obj, forWeb=False):
    try:
        if(forWeb):
            return json.encode(obj, unpicklable=False)
        else:
            return json.encode(obj)
    except:
        log_manager.warning("Couldn't convert to JSON")
        return ""

def decode_json(text):
    try:
        return json.decode(text)
    except:
        log_manager.warning("Couldn't convert to python object")
        return None

def exists(path, name):
    s = os.path.join(path, name)
    return os.path.exists(s)


#open file and return text
def open_file(path, name):
    s = os.path.join(path, name)
    try: 
        file = open(s, encoding='utf-8')
        text = file.read()
        file.close()
        log_manager.log("Opened file: ", s)
        return text
    except:
        log_manager.warning("Couldn't open file")
        return ""

#save text to the specified path, creates new if it doesn't exist
def write_file(path, name, text):
    s = os.path.join(path, name)
    try:
        file = open(s, mode='w', encoding='utf-8')
        file.write(text)
        file.flush()
        file.close()
        log_manager.log("written to/ created: ", s)
        return True
    except Exception as e:
        log_manager.warning(str(e))
        return False


def delete_file(path, name):
    try:
        s = os.path.join(path, name)
        if os.path.exists(s):
            os.remove(s)
            log_manager.log("deleted: ", s)
            return True
    except:
        log_manager.warning("Couldn't delete file")
        return False
            
"""
Imports a module and class on runtime
This function works only if the filname IS EXACTLY THE SAME 
as the classname, or give a specific classname.
Returns an attribute that can be instantiated as a class

param modulename: name of the module
param classname: OPTIONAL, name of the class to import
param pkgname: name of the package the module is in
"""
def dynamic_import_module(modulename, *, classname = "", pkgname=""):
    try:
        path = "."+pkgname+"."+modulename
        module = importlib.import_module(path , package="cosplay_manager_server")
        dynClass = None
        if classname == "":
            dynClass = getattr(module, modulename)
        else:
            dynClass = getattr(module, classname)
        return dynClass
        
    except Exception as e:
        log_manager.error(str(e))
        return None

           
        
