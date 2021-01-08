from flask_sqlalchemy import SQLAlchemy
from flask_server import app

#database initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CostumeIgniteDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def initialize():
    db.create_all()
    return True

def commit_changes():
    db.session.commit()
    return

def delete_record(record):
    db.session.delete(record)
    return

def add_record(record):
    db.session.add(record)
    return