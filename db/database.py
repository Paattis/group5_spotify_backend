import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, DateTime
from datetime import datetime
from dotenv import load_dotenv


########################################
################ SETUP #################
########################################

load_dotenv()

DB_DIALECT=os.getenv("DB_DIALECT")
DB_DRIVER=os.getenv("DB_DRIVER")
DB_PORT=os.getenv("DB_PORT")
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_NAME=os.getenv("DB_NAME")

conn_str = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db = SQLAlchemy()

def init_app(app: Flask):
    print(f'Database connection string: {conn_str}')
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from flask_migrate import Migrate

    db.init_app(app)
    migrate = Migrate(app=app, db=db)

    return db, migrate


########################################
################ MODELS ################
########################################

class DateMixin(object):
    __abstract__ = True
    created_on = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)


class Location(db.Model, DateMixin):
    __tablename__ = "Location"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return f"Location(id={self.id}, name={self.name})"

