from app.models import User, StudentGroup
from app.models import StudyProgram, Faculty
from app.models import Module, Assessment
from app.models import Enrollment
from flask_bcrypt import generate_password_hash
from datetime import datetime, time # Import time for new schedule fields
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


    # --- Module (10 total, 2 per teacher) ---
    # Fetch teachers to assign modules
    teacher = User.query.filter_by(email="teacher@mail.com").first()
    teacher2 = User.query.filter_by(email="teacher2@mail.com").first()
    teacher3 = User.query.filter_by(email="eve@mail.com").first()
    teacher4 = User.query.filter_by(email="frank.instructor@mail.com").first()
    teacher5 = User.query.filter_by(email="hannah.lecturer@mail.com").first()


    modules_to_add = [
        # Teacher 1 (Bob Teacher)
        {"name": "Algorithms and Data Structures", "description": "Core computer science fundamentals.", "credits": 6, "semester": "autumn", "day_of_week": "Monday", "start_time": time(10, 0), "end_time": time(12, 0), "program": prog, "teacher": teacher},
        {"name": "Advanced Networking", "description": "Deep dive into network protocols and design.", "credits": 6, "semester": "spring", "day_of_week": "Monday", "start_time": time(14, 0), "end_time": time(16, 0), "program": prog, "teacher": teacher},

        # Teacher 2 (Dana Teacher)
        {"name": "Databases and SQL", "description": "Relational database theory and hands-on SQL.", "credits": 6, "semester": "spring", "day_of_week": "Tuesday", "start_time": time(14, 0), "end_time": time(16, 0), "program": prog2, "teacher": teacher2},
        {"name": "Cloud Computing", "description": "Introduction to cloud platforms and services.", "credits": 5, "semester": "autumn", "day_of_week": "Tuesday", "start_time": time(10, 0), "end_time": time(12, 0), "program": prog2, "teacher": teacher2},

        # Teacher 3 (Eve Professor)
        {"name": "Object-Oriented Programming", "description": "Principles and practices of OOP.", "credits": 6, "semester": "autumn", "day_of_week": "Wednesday", "start_time": time(11, 0), "end_time": time(13, 0), "program": prog, "teacher": teacher3},
        {"name": "Software Testing", "description": "Methodologies and tools for software quality assurance.", "credits": 5, "semester": "spring", "day_of_week": "Wednesday", "start_time": time(9, 0), "end_time": time(11, 0), "program": prog, "teacher": teacher3},

        # Teacher 4 (Frank Instructor)
        {"name": "Operating Systems", "description": "Concepts of modern operating systems.", "credits": 5, "semester": "spring", "day_of_week": "Thursday", "start_time": time(9, 0), "end_time": time(11, 0), "program": prog2, "teacher": teacher4},
        {"name": "Computer Graphics", "description": "Fundamentals of rendering and animation.", "credits": 6, "semester": "autumn", "day_of_week": "Thursday", "start_time": time(13, 0), "end_time": time(15, 0), "program": prog2, "teacher": teacher4},

        # Teacher 5 (Hannah Lecturer)
        {"name": "Machine Learning Fundamentals", "description": "Introduction to ML algorithms and applications.", "credits": 7, "semester": "autumn", "day_of_week": "Friday", "start_time": time(14, 0), "end_time": time(16, 0), "program": prog, "teacher": teacher5},
        {"name": "Artificial Intelligence", "description": "Core concepts and techniques of AI.", "credits": 7, "semester": "spring", "day_of_week": "Friday", "start_time": time(10, 0), "end_time": time(12, 0), "program": prog, "teacher": teacher5},
    ]

    # Add or update modules
    for m_data in modules_to_add:
        mod_obj = Module.query.filter_by(name=m_data["name"]).first()
        if not mod_obj:
            mod_obj = Module(
                name=m_data["name"],
                description=m_data["description"],
                credits=m_data["credits"],
                semester=m_data["semester"],
                day_of_week=m_data["day_of_week"],
                start_time=m_data["start_time"],
                end_time=m_data["end_time"],
                program=m_data["program"],
                teacher=m_data["teacher"]
            )
            db.session.add(mod_obj)
        else: # Update existing module's properties if needed
            mod_obj.description = m_data["description"]
            mod_obj.credits = m_data["credits"]
            mod_obj.semester = m_data["semester"]
            mod_obj.day_of_week = m_data["day_of_week"]
            mod_obj.start_time = m_data["start_time"]
            mod_obj.end_time = m_data["end_time"]
            mod_obj.program = m_data["program"]
            mod_obj.teacher = m_data["teacher"]
    db.session.commit()

    # Fetch updated module objects for assessments and enrollments
    mod_algos = Module.query.filter_by(name="Algorithms and Data Structures").first()
    mod_net = Module.query.filter_by(name="Advanced Networking").first()
    mod_db = Module.query.filter_by(name="Databases and SQL").first()
    mod_cloud = Module.query.filter_by(name="Cloud Computing").first()
    mod_oop = Module.query.filter_by(name="Object-Oriented Programming").first()
    mod_testing = Module.query.filter_by(name="Software Testing").first()
    mod_os = Module.query.filter_by(name="Operating Systems").first()
    mod_graphics = Module.query.filter_by(name="Computer Graphics").first()
    mod_ml = Module.query.filter_by(name="Machine Learning Fundamentals").first()
    mod_ai = Module.query.filter_by(name="Artificial Intelligence").first()


    # --- Assessment ---
    # Clear existing assessments and add new ones for the 10 modules
    # Note: If you're deleting the DB each time, Assessment.query.delete() isn't strictly needed,
    # but it ensures a clean state for assessments if the script is run on an existing DB.
    # Assessment.query.delete()
    # db.session.commit()

    assessments_to_add = [
        {"module": mod_algos, "date": datetime(2025, 6, 1, 9, 0), "description": "Midterm Exam - Algorithms", "type": "egzaminas"},
        {"module": mod_algos, "date": datetime(2025, 12, 15, 10, 0), "description": "Final Project - Algorithms", "type": "projektas"},
        {"module": mod_net, "date": datetime(2026, 1, 10, 11, 0), "description": "Networking Midterm", "type": "egzaminas"},
        {"module": mod_db, "date": datetime(2025, 6, 20, 10, 0), "description": "Final Exam - Databases", "type": "egzaminas"},
        {"module": mod_db, "date": datetime(2025, 10, 10, 14, 0), "description": "SQL Practical Test", "type": "kontrolinis"},
        {"module": mod_cloud, "date": datetime(2025, 12, 1, 13, 0), "description": "Cloud Project Submission", "type": "projektas"},
        {"module": mod_oop, "date": datetime(2025, 11, 5, 11, 0), "description": "OOP Design Review", "type": "projektas"},
        {"module": mod_oop, "date": datetime(2026, 1, 20, 9, 0), "description": "OOP Final Exam", "type": "egzaminas"},
        {"module": mod_testing, "date": datetime(2026, 2, 1, 10, 0), "description": "Test Case Development", "type": "uzduotis"},
        {"module": mod_os, "date": datetime(2025, 10, 25, 13, 0), "description": "OS Midterm", "type": "egzaminas"},
        {"module": mod_os, "date": datetime(2026, 2, 15, 9, 0), "description": "Kernel Module Project", "type": "projektas"},
        {"module": mod_graphics, "date": datetime(2025, 11, 20, 14, 0), "description": "Graphics Demo", "type": "projektas"},
        {"module": mod_ml, "date": datetime(2026, 1, 10, 15, 0), "description": "ML Final Project", "type": "projektas"},
        {"module": mod_ml, "date": datetime(2025, 12, 5, 10, 0), "description": "ML Theory Exam", "type": "egzaminas"},
        {"module": mod_ai, "date": datetime(2026, 2, 20, 11, 0), "description": "AI Ethics Essay", "type": "uzduotis"},
    ]

    for a_data in assessments_to_add:
        existing_assess = Assessment.query.filter_by(
            module_id=a_data["module"].id,
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
        # Alice (Informatics)
        {"student": student_alice, "module": mod_algos, "attendance": 95.0, "grade": 9.5},
        {"student": student_alice, "module": mod_oop, "attendance": 90.0, "grade": 8.8},
        {"student": student_alice, "module": mod_ml, "attendance": 92.0, "grade": 9.1},
        {"student": student_alice, "module": mod_net, "attendance": 88.0, "grade": 8.5},

        # Charlie (Software Engineering)
        {"student": student_charlie, "module": mod_db, "attendance": 88.0, "grade": 8.7},
        {"student": student_charlie, "module": mod_os, "attendance": 85.0, "grade": 7.9},
        {"student": student_charlie, "module": mod_cloud, "attendance": 90.0, "grade": 8.6},
        {"student": student_charlie, "module": mod_testing, "attendance": 82.0, "grade": 7.5},

        # Frank (Informatics)
        {"student": student_frank, "module": mod_algos, "attendance": 92.0, "grade": 8.0},
        {"student": student_frank, "module": mod_ai, "attendance": 85.0, "grade": 7.8},
        {"student": student_frank, "module": mod_oop, "attendance": 95.0, "grade": 9.0},

        # Ivy (Informatics)
        {"student": student_ivy, "module": mod_oop, "attendance": 93.0, "grade": 9.2},
        {"student": student_ivy, "module": mod_ml, "attendance": 89.0, "grade": 8.5},
        {"student": student_ivy, "module": mod_algos, "attendance": 87.0, "grade": 8.0},

        # Jack (Software Engineering)
        {"student": student_jack, "module": mod_db, "attendance": 91.0, "grade": 9.0},
        {"student": student_jack, "module": mod_os, "attendance": 87.0, "grade": 8.1},
        {"student": student_jack, "module": mod_graphics, "attendance": 89.0, "grade": 8.3},

        # Karen (Informatics)
        {"student": student_karen, "module": mod_algos, "attendance": 88.0, "grade": 8.3},
        {"student": student_karen, "module": mod_oop, "attendance": 94.0, "grade": 9.3},
        {"student": student_karen, "module": mod_net, "attendance": 90.0, "grade": 8.7},

        # Liam (Software Engineering)
        {"student": student_liam, "module": mod_os, "attendance": 90.0, "grade": 8.6},
        {"student": student_liam, "module": mod_db, "attendance": 82.0, "grade": 7.5},
        {"student": student_liam, "module": mod_cloud, "attendance": 88.0, "grade": 8.0},

        # Mia (Informatics)
        {"student": student_mia, "module": mod_ml, "attendance": 96.0, "grade": 9.8},
        {"student": student_mia, "module": mod_algos, "attendance": 91.0, "grade": 8.9},
        {"student": student_mia, "module": mod_ai, "attendance": 94.0, "grade": 9.2},

        # Noah (Software Engineering)
        {"student": student_noah, "module": mod_db, "attendance": 85.0, "grade": 7.8},
        {"student": student_noah, "module": mod_os, "attendance": 89.0, "grade": 8.4},
        {"student": student_noah, "module": mod_graphics, "attendance": 82.0, "grade": 7.6},

        # Olivia (Informatics)
        {"student": student_olivia, "module": mod_oop, "attendance": 90.0, "grade": 8.7},
        {"student": student_olivia, "module": mod_ml, "attendance": 93.0, "grade": 9.0},
        {"student": student_olivia, "module": mod_net, "attendance": 85.0, "grade": 7.9},

        # Peter (Software Engineering)
        {"student": student_peter, "module": mod_db, "attendance": 87.0, "grade": 8.2},
        {"student": student_peter, "module": mod_os, "attendance": 91.0, "grade": 8.9},
        {"student": student_peter, "module": mod_cloud, "attendance": 84.0, "grade": 7.7},

        # Quinn (Informatics)
        {"student": student_quinn, "module": mod_algos, "attendance": 94.0, "grade": 9.6},
        {"student": student_quinn, "module": mod_oop, "attendance": 88.0, "grade": 8.1},
        {"student": student_quinn, "module": mod_ai, "attendance": 90.0, "grade": 8.5},
    ]

    for e_data in enrollments_to_add:
        if e_data["student"] and e_data["module"]:
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
