from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Integer, String, Column
from sqlalchemy_serializer import SerializerMixin
from .DateMixin import DateMixin
from db.setup import db


songs = db.Table('locationsong',
    db.Column('song_id', db.Integer, db.ForeignKey('Song.id'), primary_key=True),
    db.Column('location_id', db.Integer, db.ForeignKey('Location.id'), primary_key=True)
)

class Location(db.Model, DateMixin, SerializerMixin):
    __tablename__ = "Location"
    serialize_rules = ('-songs.locations',)

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    songs = db.relationship('Song', secondary=songs, lazy='subquery', 
        backref=db.backref('locations', lazy=True)
      )

    def __repr__(self):
        return f"Location(id={self.id}, name={self.name})"


