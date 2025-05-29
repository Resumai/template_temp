from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_bcrypt import generate_password_hash, check_password_hash



class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'student', 'teacher', 'admin'
    failed_logins = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime, nullable=True)

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id', ondelete='SET NULL'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('student_group.id', ondelete='SET NULL'), nullable=True)

    program = relationship("StudyProgram", back_populates="users", passive_deletes=True)
    group = relationship("StudentGroup", back_populates="students", passive_deletes=True)

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete")
    modules_taught = relationship("Module", back_populates="teacher")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class StudentGroup(db.Model):
    __tablename__ = 'student_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id', ondelete='SET NULL'), nullable=True)
    program = relationship("StudyProgram", back_populates="groups", passive_deletes=True)

    students = relationship("User", back_populates="group")