
from app import db
from sqlalchemy.orm import relationship



class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    attendance = db.Column(db.Float)
    grade = db.Column(db.Float)

    student = relationship("User", back_populates="enrollments")
    module = relationship("Module", back_populates="enrollments")