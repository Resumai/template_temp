from db import db
from sqlalchemy.orm import relationship

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    attendance = db.Column(db.Float)  # Lankomumas procentais
    grade = db.Column(db.Float)  # Galutinis pažymys

    student = relationship("User")
    module = relationship("Module", back_populates="enrollments")