from app import db
from app.models import User, Module, StudyProgram
from flask_bcrypt import generate_password_hash
from datetime import time

# For hardcoding admin user
# Usage example: create_admin_user()
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


# Usage example: create_new_admin_user("New Admin", "new_admin@mail.com", "password")
def create_new_admin_user(admin_name, admin_email, admin_password):
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            name=admin_name,
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            role='admin',
            program_id=None,
            group_id=None
        )
        print(f"Admin user '{admin_name}' created successfully!")
        db.session.add(admin)
        db.session.commit()
    else:
        print(f"Admin user with email '{admin_email}' already exists.")

# TODO: TEST
# Usage example: delete_user(1)
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"User ID {user_id} deleted successfully.")
    else:
        print(f"User ID {user_id} not found.")


# Usage example: add_new_module("New Module", "New Module Description", 5, "autumn", "Monday", 9, 30, 11, 0, "INFO2025", "teacher@mail.com")
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

# Another example of usage:
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


# Usage example: update_module(1, new_name="Updated Module Name")
def update_module(module_id, **kwargs: Module):
    module : Module = Module.query.get(module_id)
    if not module:
        print(f"Module ID {module_id} not found.")
        return

    for key, value in kwargs.items():
        setattr(module, key, value)
    db.session.commit()
    print(f"Module ID {module_id} updated successfully.")


# Usage example: delete_module(1)
def delete_module(module_id):
    module = Module.query.get(module_id)
    if module:
        db.session.delete(module)
        db.session.commit()
        print(f"Module ID {module_id} deleted successfully.")
    else:
        print(f"Module ID {module_id} not found.")


# Usage example: add_study_program("New Study Program", "NEW2025", 1)
def add_study_program(name, study_code, faculty_id):
    try:
        # 1. Create a new StudyProgram instance
        new_program = StudyProgram(
            name=name,
            code=study_code,
            faculty_id=faculty_id # ID of Faculty or Faculty object
        )

        # 2. Add to the session and commit
        db.session.add(new_program)
        db.session.commit()
        print(f"Study Program '{name}' added successfully!")
        return new_program

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return None


# Usage example: update_study_program(1, new_name="New Study Program Name")
def update_study_program(program_id, new_name=None, new_code=None, new_faculty_id=None):
    program = StudyProgram.query.get(program_id)

    if program:
        if new_name is not None:
            program.name = new_name
        if new_code is not None:
            program.code = new_code
        if new_faculty_id is not None:
            program.faculty_id = new_faculty_id

        db.session.commit()
        print(f"Study Program ID {program_id} updated.")
        return program
    else:
        print(f"Study Program ID {program_id} not found.")
        return None

