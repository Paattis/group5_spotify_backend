from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy_serializer import SerializerMixin
from .DateMixin import DateMixin
from db.setup import db
from datetime import datetime

"""
songs = db.Table('locationsong',
    db.Column('song_id', db.Integer, db.ForeignKey('Song.id'), primary_key=True),
    db.Column('location_id', db.Integer, db.ForeignKey('Location.id'), primary_key=True),
    db.Column('created_on', DateTime, default=datetime.now),
    db.Column('song_local_popularity', Integer, default=0),
)"""



class LocationSong(db.Model, DateMixin):
    __tablename__ = "locationsong"

    song_id = db.Column(db.Integer, db.ForeignKey('Song.id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'), primary_key=True)
    song_local_popularity = db.Column(Integer, default=0)

    def weighted_popularity(self):
      local_popularity = self.song_local_popularity or 1

      if self.created_on:
        days_since_create = (datetime.now() - self.created_on).days
      else:
        days_since_create = 0

      divide_by = int(0.1 * days_since_create)

      if divide_by < 1:
        divide_by = 1

      weighted = int(local_popularity / divide_by)

      if weighted >= local_popularity:
        return local_popularity

      return weighted

class Location(db.Model, DateMixin, SerializerMixin):
    __tablename__ = "Location"
    serialize_rules = ('-songs.locations',)

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    songs = db.relationship('Song', secondary=LocationSong.__table__, lazy='subquery', 
        backref=db.backref('locations', lazy=True)
      )

    def __repr__(self):
        return f"Location(id={self.id}, name={self.name})"


