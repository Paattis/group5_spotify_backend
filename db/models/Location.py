from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Integer, String, Column
from .DateMixin import DateMixin
from db.setup import db

class Location(db.Model, DateMixin, SerializerMixin):
    __tablename__ = "Location"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return f"Location(id={self.id}, name={self.name})"
