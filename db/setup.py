import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

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

