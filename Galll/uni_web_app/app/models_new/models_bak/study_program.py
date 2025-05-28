from db import db
from sqlalchemy.orm import relationship

class StudyProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="programs")

    users = relationship("User", back_populates="program")
    groups = relationship("StudentGroup", back_populates="program")
    modules = relationship("Module", back_populates="program")