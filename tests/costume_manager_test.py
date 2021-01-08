from backend import costume_manager 
from backend.costume_manager import Costume, CostumePart, PixelRange
from backend import g_costume_manager as cosman
from backend import log_manager

from backend import file_manager as fm
"""
File management
"""
class JTest():
    name = ''
    name2 = 0
    planet = ''
    universe = ''

    newname = ''
    def __init__(self):
        pass


def Test():
    T1name = "TestCostume1"
    T2name = "TestCostume2"
    TestCostume1 = cosman.create_and_save_new_costume(name=T1name)
    TestCostume2 = cosman.create_and_save_new_costume(name=T2name)
    
    #test get_costumes
    cos_list = cosman.get_costumes()
    names_list = cos_list.values()
    assert len(cos_list) > 0
    
    #test create costume and save func
    assert T1name in names_list
    assert T2name in names_list

    #test deletion
    cosman.delete_costume(TestCostume1.id)
    cosman.delete_costume(TestCostume2.id)

    cos_list = cosman.get_costumes()#refresh list 
    key_list = cos_list.keys()
    assert TestCostume1.id not in key_list
    assert TestCostume2.id not in key_list



# def TestJson():
#     """
#     Tests loading and saving of costume
#     """
#     #init costume part
#     costume_manager_sub = g_costume_manager
#     arm = CostumePart("arm_R", GPIOPin.D18)
#     costume_manager.set_pixel_range(arm, PixelRange(0, 299))

#     #init costume
#     cos = Costume("TestCostume")
#     costume_manager.set_costume(costume_manager_sub, cos)
#     costume_manager.add_costume_part(costume_manager_sub, arm)
#     costume_manager.add_pixel_strip(costume_manager_sub, GPIOPin.D18, 300)

#     #saving costume
#     costume_manager.save_costume(costume_manager_sub)

#     #unload then load saved
#     costume_manager.unload_costume(costume_manager_sub)
#     costume_manager.load_costume(costume_manager_sub, cos.name)

#     #checking loaded values
#     loaded = costume_manager_sub.loaded_costume
#     assert loaded.name == cos.name
#     assert loaded.costume_parts[0].name == cos.costume_parts[0].name
#     assert loaded.costume_parts[0].pixel_range.begin == cos.costume_parts[0].pixel_range.begin
#     assert loaded.costume_parts[0].pixel_range.end == cos.costume_parts[0].pixel_range.end
#     assert loaded.costume_parts[0].pin == cos.costume_parts[0].pin

#     #removing values
#     costume_manager.remove_costume_part(costume_manager_sub, cos.costume_parts[0].name)
#     costume_manager.remove_pixel_strip(costume_manager_sub, GPIOPin.D18)

#     #checking values
#     loaded = costume_manager_sub.loaded_costume #to be sure
#     assert len(loaded.costume_parts) == 0
#     assert len(loaded.pixel_strips) == 0

#     log_manager.testlog("costume_manager passed all tests")
#     pass    

# from flask_server.database_manager import db
# from backend.database_classes import Costume_DB
# from backend.database_classes import CostumePart_DB
# from backend.database_classes import CostumePixelStrip_DB

# from backend.database_classes import TestDatabaseRow_DB

# def DatabaseTest():
#     testcolumn1 = TestDatabaseRow_DB(name="O ChinChin", name2="The ZUCC", name3="Tap-Brothers")

#     #db.session.add(testcolumn1)
#     #db.session.commit()
#     retrieved1 = TestDatabaseRow_DB.query.all()
#     retrieved1 = retrieved1[0]
#     retrieved1.name = "Pink Guy"
#     retrieved1.name2 = "Francis of the Filth"
#     retrieved1.name3 = "Filthy Frank"

#     #db.session.add(retrieved1)
#     db.session.commit()

#     retrieved2 = TestDatabaseRow_DB.query.all()
#     print("")

#     g_costume_manager.get_costume_name_id_dict()
#     g_costume_manager.load_costume(1)

#     g_costume_manager.current_costume.get_name()
#     g_costume_manager.current_costume.get_parts_name_id_dict()
#     g_costume_manager.current_costume.get_pixel_strip_records()

    
    # #init costume part
    # arm = CostumePart("arm_R", GPIOPin.D18)
    # costume_manager.set_pixel_range(arm, PixelRange(0, 299))

    # #init costume
    # cos = Costume("TestCostume")
    # costume_manager.set_costume(g_costume_manager, cos)
    # costume_manager.add_costume_part(g_costume_manager, arm)
    # costume_manager.add_pixel_strip(g_costume_manager, GPIOPin.D18, 300)

    # #save costume
    # costumepart_db = CostumePart_DB(name=arm.name, pixelrange_begin=arm.pixel_range.begin, pixelrange_end=arm.pixel_range.end, pin=arm.pin.value)
    # pixelstrip_db = CostumePixelStrip_DB(gpio_pin=GPIOPin.D18.value, count=cos.pixel_strips[GPIOPin.D18.value])
    
    # costume_db = Costume_DB(name=cos.name)
    # costume_db.costume_parts.append(costumepart_db)
    # costume_db.pixel_strips.append(pixelstrip_db)

    # db.session.add(costume_db)
    # db.session.add(costumepart_db)
    # db.session.add(pixelstrip_db)
    # db.session.commit()

    # retreived = Costume_DB.query.filter_by(name="TestCostume").first()
    # assert retreived.name == cos.name

def TestAll():
    Test()