from app import db
from sqlalchemy.orm import relationship


class StudentGroup(db.Model):
    __tablename__ = 'student_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id', ondelete='SET NULL'), nullable=True)
    program = relationship("StudyProgram", back_populates="groups", passive_deletes=True)

    students = relationship("User", back_populates="group")