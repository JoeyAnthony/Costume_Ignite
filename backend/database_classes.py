from flask_server.database_manager import db
from flask_server.database_manager import add_record, delete_record, commit_changes


"""
To update to new database versions:
Create json export of the whole database with the old version
Import with the new one and save
"""
 
"""IgniteSettings"""
class IgniteConfig_DB(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    config_name = db.Column(db.String(30), nullable = False)
    active_library = db.Column(db.String(20))
    pass

"""CostumeManager"""
#CostumeParts have a dict with [presetname][scriptname]
#When turning on a preset
#class CostumePreset(db.Model):
#    presetName = db.Column(db.Integer, nullable = False)

class Costume_DB(db.Model):
    __tablename__ = 'costumes'
    id = db.Column(db.Integer, primary_key=True)
    #Name of the suit
    name = db.Column(db.String(30), nullable = False)
    #Array of SuitParts
    costume_parts = db.relationship('CostumePart_DB', backref='costumes', lazy=True)
    #list of GPIOPins with ledcounts
    pixel_strips = db.relationship('CostumePixelStrip_DB', backref='costumes', lazy=True)

class CostumePart_DB(db.Model):
    __tablename__ = 'costumeparts'
    id = db.Column(db.Integer, primary_key=True)
    #Name of the component
    name = db.Column(db.String(30), nullable = False)  
    #element range on the ledstrip
    pixelrange_begin = db.Column(db.Integer, nullable = False)
    pixelrange_end = db.Column(db.Integer, nullable = False)
    #neopixel pin this component is assigned to
    pin = db.Column(db.String(30), nullable = False)
    #costume this part belongs to
    costume_id = db.Column(db.Integer, db.ForeignKey('costumes.id'))

class CostumePixelStrip_DB(db.Model):
    __tablename__ = 'pixelstrips'
    id = db.Column(db.Integer, primary_key=True)
    #gpio pin
    gpio_pin = db.Column(db.String(3), nullable=False)
    #led count
    count = db.Column(db.Integer, nullable=False)

    #costume this ledstrip belongs to
    costume_id = db.Column(db.Integer, db.ForeignKey('costumes.id'))

class TestDatabaseRow_DB(db.Model):
    __tablename__ = 'testrow'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False)
    name2 = db.Column(db.String(30), nullable=False)
    name3 = db.Column(db.String(30), nullable=False)