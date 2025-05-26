from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime as dt
from db import db


class Student(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    year = Column(Integer)
    color = Column(String(32))
    vin = Column(String(128))
    created_at = Column(DateTime, default=dt.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)