from sqlalchemy import Column, DateTime
from datetime import datetime

class DateMixin(object):
    __abstract__ = True
    created_on = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)