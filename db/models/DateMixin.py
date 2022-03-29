from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.types import DateTime

from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DateMixin(object):
  __abstract__ = True

  created_on = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, onupdate=datetime.now)