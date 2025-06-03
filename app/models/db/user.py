from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'student', 'teacher', 'admin'
    profile_picture = db.Column(db.String(200))

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id', ondelete='SET NULL'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('student_group.id', ondelete='SET NULL'), nullable=True)

    program = relationship("StudyProgram", back_populates="users", passive_deletes=True)
    group = relationship("StudentGroup", back_populates="students", passive_deletes=True)

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete")
    modules_taught = relationship("Module", back_populates="teacher")

    failed_logins = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime, nullable=True)
    block_reason = db.Column(db.String(200), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_temporarily_blocked(self):
        """Check if user is currently blocked."""
        return self.blocked_until and self.blocked_until > datetime.utcnow()

    def block_for_minutes(self, minutes=5, reason="Too many failed login attempts"):
        """Block user for a specified number of minutes with optional reason."""
        self.blocked_until = datetime.utcnow() + timedelta(minutes=minutes)
        self.block_reason = reason

    def clear_block(self):
        """This clears the user's block and reset failed logins."""
        self.failed_logins = 0
        self.blocked_until = None
        self.block_reason = None

    def get_remaining_block_minutes(self):
        """Get remaining block time in mins."""
        if self.is_temporarily_blocked():
            return 0
        remaining = self.blocked_until - datetime.utcnow()
        return max(0, int(remaining.total_seconds() / 60))
 
