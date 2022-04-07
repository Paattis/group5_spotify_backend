from sqlalchemy import Integer, String, Column, DateTime
from .DateMixin import DateMixin
from db.setup import db

class AccessToken(db.Model, DateMixin):

    """Summary
    
    Attributes:
        id (Column<Integer>): the primary key
        access_token (Column<String>): the access token to store
        expire_date (Column<DateTime>): the time the access token will expire
    """

    __tablename__ = "AccessToken"
    id = Column(Integer, primary_key=True)
    access_token = Column(String(255))
    expire_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"AccessToken(id={self.id}, name={self.access_token})"
