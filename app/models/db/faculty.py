from app import db
from sqlalchemy.orm import relationship


class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    programs = relationship("StudyProgram", back_populates="faculty")