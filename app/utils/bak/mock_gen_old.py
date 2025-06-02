from app.models.user import User, StudentGroup
from app.models.study_program import StudyProgram, Faculty
from app.models.module import Module, Assessment
from app.models.enrollment import Enrollment
from flask_bcrypt import generate_password_hash
from datetime import datetime
from app import db


# Generation of mock data for testing DB related functionality
def generate_mock_data():
    # --- Faculty ---
    if not Faculty.query.first():
        fac = Faculty(name="Faculty of Engineering")
        db.session.add(fac)
        db.session.commit()
    else:
        fac = Faculty.query.first()

    # Additional faculty
    if not Faculty.query.filter_by(name="Faculty of Science").first():
        fac2 = Faculty(name="Faculty of Science")
        db.session.add(fac2)
        db.session.commit()
    else:
        fac2 = Faculty.query.filter_by(name="Faculty of Science").first()

    # --- Study Program ---
    if not StudyProgram.query.first():
        prog = StudyProgram(name="Informatics", code="INFO2025", faculty=fac)
        db.session.add(prog)
        db.session.commit()
    else:
        prog = StudyProgram.query.first()

    if not StudyProgram.query.filter_by(code="SOFT2025").first():
        prog2 = StudyProgram(name="Software Engineering", code="SOFT2025", faculty=fac2)
        db.session.add(prog2)
        db.session.commit()
    else:
        prog2 = StudyProgram.query.filter_by(code="SOFT2025").first()

    # --- Student Group ---
    if not StudentGroup.query.first():
        group = StudentGroup(name="INFO-22-A", program=prog)
        db.session.add(group)
        db.session.commit()
    else:
        group = StudentGroup.query.first()

    if not StudentGroup.query.filter_by(name="SOFT-22-B").first():
        group2 = StudentGroup(name="SOFT-22-B", program=prog2)
        db.session.add(group2)
        db.session.commit()
    else:
        group2 = StudentGroup.query.filter_by(name="SOFT-22-B").first()

    # --- Users ---
    if not User.query.filter_by(email="student@mail.com").first():
        student = User(
            name="Alice Student",
            email="student@mail.com",
            password_hash=generate_password_hash("password"),
            role="student",
            program=prog,
            group=group
        )
        db.session.add(student)

    if not User.query.filter_by(email="teacher@mail.com").first():
        teacher = User(
            name="Bob Teacher",
            email="teacher@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog
        )
        db.session.add(teacher)

    if not User.query.filter_by(email="student2@mail.com").first():
        student2 = User(
            name="Charlie Student",
            email="student2@mail.com",
            password_hash=generate_password_hash("password"),
            role="student",
            program=prog2,
            group=group2
        )
        db.session.add(student2)

    if not User.query.filter_by(email="teacher2@mail.com").first():
        teacher2 = User(
            name="Dana Teacher",
            email="teacher2@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog2
        )
        db.session.add(teacher2)

    db.session.commit()

    # --- Module ---
    if not Module.query.first():
        mod = Module(
            name="Algorithms and Data Structures",
            description="Core computer science fundamentals.",
            credits=6,
            semester="rudens",
            schedule="Mon 10:00-12:00",
            program=prog,
            teacher=teacher
        )
        db.session.add(mod)
        db.session.commit()
    else:
        mod = Module.query.first()

    if not Module.query.filter_by(name="Databases and SQL").first():
        mod2 = Module(
            name="Databases and SQL",
            description="Relational database theory and hands-on SQL.",
            credits=6,
            semester="pavasario",
            schedule="Tue 14:00-16:00",
            program=prog2,
            teacher=teacher2
        )
        db.session.add(mod2)
        db.session.commit()
    else:
        mod2 = Module.query.filter_by(name="Databases and SQL").first()

    # --- Assessment ---
    if not Assessment.query.first():
        assess = Assessment(
            module=mod,
            date=datetime(2025, 6, 1, 9, 0),
            description="Midterm Exam",
            type="egzaminas"
        )
        db.session.add(assess)
        db.session.commit()

    if not Assessment.query.filter_by(description="Final Exam").first():
        assess2 = Assessment(
            module=mod2,
            date=datetime(2025, 6, 20, 10, 0),
            description="Final Exam",
            type="egzaminas"
        )
        db.session.add(assess2)
        db.session.commit()

    # --- Enrollment ---
    student = User.query.filter_by(email="student@mail.com").first()
    if student and not Enrollment.query.filter_by(student_id=student.id, module_id=mod.id).first():
        enrollment = Enrollment(
            student=student,
            module=mod,
            attendance=95.0,
            grade=9.5
        )
        db.session.add(enrollment)

    student2 = User.query.filter_by(email="student2@mail.com").first()
    if student2 and not Enrollment.query.filter_by(student_id=student2.id, module_id=mod2.id).first():
        enrollment2 = Enrollment(
            student=student2,
            module=mod2,
            attendance=88.0,
            grade=8.7
        )
        db.session.add(enrollment2)

    db.session.commit()
