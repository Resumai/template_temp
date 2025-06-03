from app import db
from app.models import User, Module, StudyProgram
from flask_bcrypt import generate_password_hash
from datetime import time

def create_admin_user():
    if not User.query.filter_by(email='admin@mail.com').first():
        admin = User(
            name='Admin',
            email='admin@mail.com',
            password_hash=generate_password_hash('password'),
            role='admin',
            program_id=None,
            group_id=None
        )
        db.session.add(admin)
        db.session.commit()



def add_new_module(name, description, credits, semester, day_of_week,
                   start_hour, start_minute, end_hour, end_minute,
                   program_code, teacher_email):
    try:
        # 1. Retrieve related objects
        program = StudyProgram.query.filter_by(code=program_code).first()
        if not program:
            print(f"Error: Study Program with code '{program_code}' not found.")
            return None

        teacher = User.query.filter_by(email=teacher_email, role="teacher").first()
        if not teacher:
            print(f"Error: Teacher with email '{teacher_email}' not found.")
            return None

        # Convert time components to datetime.time objects
        start_time_obj = time(start_hour, start_minute)
        end_time_obj = time(end_hour, end_minute)

        # 2. Create a new Module instance
        new_module = Module(
            name=name,
            description=description,
            credits=credits,
            semester=semester,
            day_of_week=day_of_week,
            start_time=start_time_obj,
            end_time=end_time_obj,
            program=program,  # Assign the program object
            teacher=teacher   # Assign the teacher object
        )

        # 3. Add to the session and commit
        db.session.add(new_module)
        db.session.commit()
        print(f"Module '{name}' added successfully!")
        return new_module

    except Exception as e:
        db.session.rollback() # Rollback in case of error, not sure if it does anything, would need a test
        print(f"An error occurred: {e}")
        return None

# Example usage:
# if not Module.query.filter_by(name='New Advanced Python').first():
#     add_new_module(
#         name="New Advanced Python",
#         description="Advanced topics in Python programming.",
#         credits=5,
#         semester="autumn",
#         day_of_week="Wednesday",
#         start_hour=9,
#         start_minute=30,
#         end_hour=11,
#         end_minute=0,
#         program_code="INFO2025",
#         teacher_email="teacher@mail.com"
#     )