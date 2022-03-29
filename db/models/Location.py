from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from . import DateMixin

Base = declarative_base()

class Location(Base, DateMixin):
    __tablename__ = "Location"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return f"Location(id={self.id}, name={self.name})"

