from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'teacher', 'admin'
    failed_logins = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime, nullable=True)

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('student_group.id'))

    program = relationship("StudyProgram", back_populates="users")
    group = relationship("StudentGroup", back_populates="students")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)