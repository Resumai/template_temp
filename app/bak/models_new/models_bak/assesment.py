from db import db
from sqlalchemy.orm import relationship

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    date = db.Column(db.DateTime)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50))  # Egzaminas, laboratorinis, testas

    module = relationship("Module", back_populates="assessments")