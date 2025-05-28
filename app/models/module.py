
from app import db
from sqlalchemy.orm import relationship



prerequisites = db.Table(
    'prerequisites',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('prerequisite_id', db.Integer, db.ForeignKey('module.id'))
)


class Module(db.Model):
    __tablename__ = 'module'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10))
    schedule = db.Column(db.String(200))

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)

    program = relationship("StudyProgram", back_populates="modules")
    teacher = relationship("User", back_populates="modules_taught", foreign_keys=[teacher_id], passive_deletes=True)

    assessments = relationship("Assessment", back_populates="module", cascade="all, delete")
    enrollments = relationship("Enrollment", back_populates="module", cascade="all, delete")
    prerequisites = relationship(
        "Module",
        secondary=prerequisites,
        primaryjoin=id == prerequisites.c.module_id,
        secondaryjoin=id == prerequisites.c.prerequisite_id,
        backref="required_for"
    )


class Assessment(db.Model):
    __tablename__ = 'assessment'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    date = db.Column(db.DateTime)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50))

    module = relationship("Module", back_populates="assessments")