from app import db
from app.models.user import StudentGroup

def get_or_create_group(program):
    group = StudentGroup.query.filter_by(program=program).first()
    if not group:
        group = StudentGroup(name=f"{program.name}-Group", program=program)
        db.session.add(group)
        db.session.commit()
    return group
