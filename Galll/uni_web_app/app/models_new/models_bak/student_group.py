from db import db
from sqlalchemy.orm import relationship


class StudentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # Pvz.: IFIN-18-A

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))
    program = relationship("StudyProgram", back_populates="groups")

    students = relationship("User", back_populates="group")
