from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Integer, String, Column
from .DateMixin import DateMixin
from db.setup import db

class Song(db.Model, DateMixin, SerializerMixin):
    __tablename__ = "Song"
    id = Column(Integer, primary_key=True)
    spotifyId = Column(String(255), nullable=True)
    name = Column(String(255))
    popularity = Column(Integer, default=0)

    def __repr__(self):
        return f"Song(id={self.id}, name={self.name}, popularity={self.popularity}, spotifyId={self.spotifyId})"
