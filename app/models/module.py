from db import db
from sqlalchemy.orm import relationship

prerequisites = db.Table('prerequisites',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('prerequisite_id', db.Integer, db.ForeignKey('module.id'))
)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10))  # 'rudens', 'pavasario'
    schedule = db.Column(db.String(200))

    program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    program = relationship("StudyProgram", back_populates="modules")
    teacher = relationship("User", foreign_keys=[teacher_id])

    assessments = relationship("Assessment", back_populates="module")
    enrollments = relationship("Enrollment", back_populates="module")
    prerequisites = relationship(
        "Module",
        secondary=prerequisites,
        primaryjoin=id == prerequisites.c.module_id,
        secondaryjoin=id == prerequisites.c.prerequisite_id,
        backref="required_for"
    )
