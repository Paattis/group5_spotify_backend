import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

DB_DIALECT=os.getenv("DB_DIALECT")
DB_DRIVER=os.getenv("DB_DRIVER")
DB_PORT=os.getenv("DB_PORT")
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_NAME=os.getenv("DB_NAME")


print(DB_DIALECT, DB_DRIVER, DB_PORT, DB_HOST, DB_USER, DB_PASS)
Base = declarative_base()

engine = create_engine(f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


