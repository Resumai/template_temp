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
    # Ensure only two faculties exist
    fac = Faculty.query.filter_by(name="Faculty of Engineering").first()
    if not fac:
        fac = Faculty(name="Faculty of Engineering")
        db.session.add(fac)
        db.session.commit()

    fac2 = Faculty.query.filter_by(name="Faculty of Science").first()
    if not fac2:
        fac2 = Faculty(name="Faculty of Science")
        db.session.add(fac2)
        db.session.commit()

    # --- Study Program ---
    # Ensure programs are linked to the two faculties
    prog = StudyProgram.query.filter_by(code="INFO2025").first()
    if not prog:
        prog = StudyProgram(name="Informatics", code="INFO2025", faculty=fac)
        db.session.add(prog)
        db.session.commit()
    elif prog.faculty != fac: # Update faculty if it changed
        prog.faculty = fac
        db.session.commit()

    prog2 = StudyProgram.query.filter_by(code="SOFT2025").first()
    if not prog2:
        prog2 = StudyProgram(name="Software Engineering", code="SOFT2025", faculty=fac2)
        db.session.add(prog2)
        db.session.commit()
    elif prog2.faculty != fac2: # Update faculty if it changed
        prog2.faculty = fac2
        db.session.commit()


    # --- Student Group ---
    # Existing Group 1
    group = StudentGroup.query.filter_by(name="INFO-22-A").first()
    if not group:
        group = StudentGroup(name="INFO-22-A", program=prog)
        db.session.add(group)
    elif group.program != prog:
        group.program = prog
    db.session.commit()

    # Existing Group 2
    group2 = StudentGroup.query.filter_by(name="SOFT-22-B").first()
    if not group2:
        group2 = StudentGroup(name="SOFT-22-B", program=prog2)
        db.session.add(group2)
    elif group2.program != prog2:
        group2.program = prog2
    db.session.commit()

    # New Student Group 3
    group3 = StudentGroup.query.filter_by(name="INFO-23-A").first()
    if not group3:
        group3 = StudentGroup(name="INFO-23-A", program=prog)
        db.session.add(group3)
    elif group3.program != prog:
        group3.program = prog
    db.session.commit()

    # New Student Group 4
    group4 = StudentGroup.query.filter_by(name="SOFT-23-B").first()
    if not group4:
        group4 = StudentGroup(name="SOFT-23-B", program=prog2)
        db.session.add(group4)
    elif group4.program != prog2:
        group4.program = prog2
    db.session.commit()

    # New Student Group 5
    group5 = StudentGroup.query.filter_by(name="INFO-24-A").first()
    if not group5:
        group5 = StudentGroup(name="INFO-24-A", program=prog)
        db.session.add(group5)
    elif group5.program != prog:
        group5.program = prog
    db.session.commit()


    # --- Users (Teachers - 5 total) ---
    # Existing Teacher 1
    teacher = User.query.filter_by(email="teacher@mail.com").first()
    if not teacher:
        teacher = User(
            name="Bob Teacher",
            email="teacher@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog
        )
        db.session.add(teacher)
    elif teacher.program != prog:
        teacher.program = prog
    db.session.commit()

    # Existing Teacher 2
    teacher2 = User.query.filter_by(email="teacher2@mail.com").first()
    if not teacher2:
        teacher2 = User(
            name="Dana Teacher",
            email="teacher2@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog2
        )
        db.session.add(teacher2)
    elif teacher2.program != prog2:
        teacher2.program = prog2
    db.session.commit()

    # Teacher 3 (was Eve Professor) - re-assign to prog
    teacher3 = User.query.filter_by(email="eve@mail.com").first()
    if not teacher3:
        teacher3 = User(
            name="Eve Professor",
            email="eve@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog # Assign to existing program
        )
        db.session.add(teacher3)
    elif teacher3.program != prog:
        teacher3.program = prog
    db.session.commit()

    # New Teacher 4
    teacher4 = User.query.filter_by(email="frank.instructor@mail.com").first()
    if not teacher4:
        teacher4 = User(
            name="Frank Instructor",
            email="frank.instructor@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog2 # Assign to existing program
        )
        db.session.add(teacher4)
    elif teacher4.program != prog2:
        teacher4.program = prog2
    db.session.commit()

    # New Teacher 5
    teacher5 = User.query.filter_by(email="hannah.lecturer@mail.com").first()
    if not teacher5:
        teacher5 = User(
            name="Hannah Lecturer",
            email="hannah.lecturer@mail.com",
            password_hash=generate_password_hash("password"),
            role="teacher",
            program=prog # Assign to existing program
        )
        db.session.add(teacher5)
    elif teacher5.program != prog:
        teacher5.program = prog
    db.session.commit()


    # --- Users (Students - 12 total) ---
    students_to_add = [
        {"name": "Alice Student", "email": "student@mail.com", "program": prog, "group": group},
        {"name": "Charlie Student", "email": "student2@mail.com", "program": prog2, "group": group2},
        {"name": "Frank Learner", "email": "frank@mail.com", "program": prog, "group": group3},
        {"name": "Ivy Green", "email": "ivy@mail.com", "program": prog, "group": group},
        {"name": "Jack Black", "email": "jack@mail.com", "program": prog2, "group": group2},
        {"name": "Karen White", "email": "karen@mail.com", "program": prog, "group": group3},
        {"name": "Liam Brown", "email": "liam@mail.com", "program": prog2, "group": group4},
        {"name": "Mia Grey", "email": "mia@mail.com", "program": prog, "group": group5},
        {"name": "Noah Blue", "email": "noah@mail.com", "program": prog2, "group": group4},
        {"name": "Olivia Red", "email": "olivia@mail.com", "program": prog, "group": group5},
        {"name": "Peter Yellow", "email": "peter@mail.com", "program": prog2, "group": group2},
        {"name": "Quinn Purple", "email": "quinn@mail.com", "program": prog, "group": group}
    ]

    for s_data in students_to_add:
        student_obj = User.query.filter_by(email=s_data["email"]).first()
        if not student_obj:
            student_obj = User(
                name=s_data["name"],
                email=s_data["email"],
                password_hash=generate_password_hash("password"),
                role="student",
                program=s_data["program"],
                group=s_data["group"]
            )
            db.session.add(student_obj)
        else: # Update existing student's program/group if needed
            if student_obj.program != s_data["program"]:
                student_obj.program = s_data["program"]
            if student_obj.group != s_data["group"]:
                student_obj.group = s_data["group"]
    db.session.commit()


    # --- Module (5 total, one per teacher) ---
    # Existing Module 1
    mod = Module.query.filter_by(name="Algorithms and Data Structures").first()
    if not mod:
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
    elif mod.teacher != teacher or mod.program != prog:
        mod.teacher = teacher
        mod.program = prog
    db.session.commit()

    # Existing Module 2
    mod2 = Module.query.filter_by(name="Databases and SQL").first()
    if not mod2:
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
    elif mod2.teacher != teacher2 or mod2.program != prog2:
        mod2.teacher = teacher2
        mod2.program = prog2
    db.session.commit()

    # New Module 3 (for teacher3)
    mod5 = Module.query.filter_by(name="Object-Oriented Programming").first()
    if not mod5:
        mod5 = Module(
            name="Object-Oriented Programming",
            description="Principles and practices of OOP.",
            credits=6,
            semester="rudens",
            schedule="Wed 11:00-13:00",
            program=prog,
            teacher=teacher3
        )
        db.session.add(mod5)
    elif mod5.teacher != teacher3 or mod5.program != prog:
        mod5.teacher = teacher3
        mod5.program = prog
    db.session.commit()

    # New Module 4 (for teacher4)
    mod6 = Module.query.filter_by(name="Operating Systems").first()
    if not mod6:
        mod6 = Module(
            name="Operating Systems",
            description="Concepts of modern operating systems.",
            credits=5,
            semester="pavasario",
            schedule="Thu 09:00-11:00",
            program=prog2,
            teacher=teacher4
        )
        db.session.add(mod6)
    elif mod6.teacher != teacher4 or mod6.program != prog2:
        mod6.teacher = teacher4
        mod6.program = prog2
    db.session.commit()

    # New Module 5 (for teacher5)
    mod7 = Module.query.filter_by(name="Machine Learning Fundamentals").first()
    if not mod7:
        mod7 = Module(
            name="Machine Learning Fundamentals",
            description="Introduction to ML algorithms and applications.",
            credits=7,
            semester="rudens",
            schedule="Fri 14:00-16:00",
            program=prog,
            teacher=teacher5
        )
        db.session.add(mod7)
    elif mod7.teacher != teacher5 or mod7.program != prog:
        mod7.teacher = teacher5
        mod7.program = prog
    db.session.commit()


    # --- Assessment ---
    # Fetch modules again to ensure they are up-to-date
    mod = Module.query.filter_by(name="Algorithms and Data Structures").first()
    mod2 = Module.query.filter_by(name="Databases and SQL").first()
    mod5 = Module.query.filter_by(name="Object-Oriented Programming").first()
    mod6 = Module.query.filter_by(name="Operating Systems").first()
    mod7 = Module.query.filter_by(name="Machine Learning Fundamentals").first()

    assessments_to_add = [
        {"module": mod, "date": datetime(2025, 6, 1, 9, 0), "description": "Midterm Exam - Algorithms", "type": "egzaminas"},
        {"module": mod, "date": datetime(2025, 12, 15, 10, 0), "description": "Final Project - Algorithms", "type": "projektas"},
        {"module": mod2, "date": datetime(2025, 6, 20, 10, 0), "description": "Final Exam - Databases", "type": "egzaminas"},
        {"module": mod2, "date": datetime(2025, 10, 10, 14, 0), "description": "SQL Practical Test", "type": "kontrolinis"},
        {"module": mod5, "date": datetime(2025, 11, 5, 11, 0), "description": "OOP Design Review", "type": "projektas"},
        {"module": mod5, "date": datetime(2026, 1, 20, 9, 0), "description": "OOP Final Exam", "type": "egzaminas"},
        {"module": mod6, "date": datetime(2025, 10, 25, 13, 0), "description": "OS Midterm", "type": "egzaminas"},
        {"module": mod7, "date": datetime(2026, 1, 10, 15, 0), "description": "ML Final Project", "type": "projektas"},
    ]

    for a_data in assessments_to_add:
        # Check if an assessment with the same module and description already exists
        existing_assess = Assessment.query.filter_by(
            module=a_data["module"],
            description=a_data["description"]
        ).first()
        if not existing_assess:
            assess = Assessment(
                module=a_data["module"],
                date=a_data["date"],
                description=a_data["description"],
                type=a_data["type"]
            )
            db.session.add(assess)
    db.session.commit()


    # --- Enrollment ---
    # Fetch updated student objects
    student_alice = User.query.filter_by(email="student@mail.com").first()
    student_charlie = User.query.filter_by(email="student2@mail.com").first()
    student_frank = User.query.filter_by(email="frank@mail.com").first()
    student_ivy = User.query.filter_by(email="ivy@mail.com").first()
    student_jack = User.query.filter_by(email="jack@mail.com").first()
    student_karen = User.query.filter_by(email="karen@mail.com").first()
    student_liam = User.query.filter_by(email="liam@mail.com").first()
    student_mia = User.query.filter_by(email="mia@mail.com").first()
    student_noah = User.query.filter_by(email="noah@mail.com").first()
    student_olivia = User.query.filter_by(email="olivia@mail.com").first()
    student_peter = User.query.filter_by(email="peter@mail.com").first()
    student_quinn = User.query.filter_by(email="quinn@mail.com").first()

    enrollments_to_add = [
        # Alice in Algorithms, OOP, ML
        {"student": student_alice, "module": mod, "attendance": 95.0, "grade": 9.5},
        {"student": student_alice, "module": mod5, "attendance": 90.0, "grade": 8.8},
        {"student": student_alice, "module": mod7, "attendance": 92.0, "grade": 9.1},

        # Charlie in Databases, OS
        {"student": student_charlie, "module": mod2, "attendance": 88.0, "grade": 8.7},
        {"student": student_charlie, "module": mod6, "attendance": 85.0, "grade": 7.9},

        # Frank in Algorithms, Databases
        {"student": student_frank, "module": mod, "attendance": 92.0, "grade": 8.0},
        {"student": student_frank, "module": mod2, "attendance": 80.0, "grade": 7.2},

        # Ivy in OOP, ML
        {"student": student_ivy, "module": mod5, "attendance": 93.0, "grade": 9.2},
        {"student": student_ivy, "module": mod7, "attendance": 89.0, "grade": 8.5},

        # Jack in Databases, OS
        {"student": student_jack, "module": mod2, "attendance": 91.0, "grade": 9.0},
        {"student": student_jack, "module": mod6, "attendance": 87.0, "grade": 8.1},

        # Karen in Algorithms, OOP
        {"student": student_karen, "module": mod, "attendance": 88.0, "grade": 8.3},
        {"student": student_karen, "module": mod5, "attendance": 94.0, "grade": 9.3},

        # Liam in OS, Databases
        {"student": student_liam, "module": mod6, "attendance": 90.0, "grade": 8.6},
        {"student": student_liam, "module": mod2, "attendance": 82.0, "grade": 7.5},

        # Mia in ML, Algorithms
        {"student": student_mia, "module": mod7, "attendance": 96.0, "grade": 9.8},
        {"student": student_mia, "module": mod, "attendance": 91.0, "grade": 8.9},

        # Noah in Databases, OS
        {"student": student_noah, "module": mod2, "attendance": 85.0, "grade": 7.8},
        {"student": student_noah, "module": mod6, "attendance": 89.0, "grade": 8.4},

        # Olivia in OOP, ML
        {"student": student_olivia, "module": mod5, "attendance": 90.0, "grade": 8.7},
        {"student": student_olivia, "module": mod7, "attendance": 93.0, "grade": 9.0},

        # Peter in Databases, OS
        {"student": student_peter, "module": mod2, "attendance": 87.0, "grade": 8.2},
        {"student": student_peter, "module": mod6, "attendance": 91.0, "grade": 8.9},

        # Quinn in Algorithms, OOP
        {"student": student_quinn, "module": mod, "attendance": 94.0, "grade": 9.6},
        {"student": student_quinn, "module": mod5, "attendance": 88.0, "grade": 8.1},
    ]

    for e_data in enrollments_to_add:
        if e_data["student"] and e_data["module"]: # Ensure student and module objects exist
            # Check if enrollment already exists before adding
            existing_enrollment = Enrollment.query.filter_by(
                student_id=e_data["student"].id,
                module_id=e_data["module"].id
            ).first()
            if not existing_enrollment:
                enrollment = Enrollment(
                    student=e_data["student"],
                    module=e_data["module"],
                    attendance=e_data["attendance"],
                    grade=e_data["grade"]
                )
                db.session.add(enrollment)
    db.session.commit()
