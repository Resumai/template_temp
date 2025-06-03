from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from app import db, User, Module, Enrollment
from app.utils.auth_utils import roles_required
from app.utils.data_ops import add_new_module
from datetime import datetime


teacher_bp = Blueprint('teacher', __name__)

# Convert time string to datetime.time object
def convert_to_time(time_str):
    # Check if the time string only contains the hour and add minutes ":00" if necessary
    if len(time_str.split(':')) == 1:  # Only the hour is present
        time_str += ":00"  # Add ":00" to make it valid for '%H:%M' format
    return datetime.strptime(time_str, '%H:%M').time()


### Teacher routes ###
@teacher_bp.route('/teacher-dashboard')
@roles_required('teacher')
def teacher_dashboard():
    return render_template('teacher/dashboard.html')

@teacher_bp.route('/assign_modules', methods=['GET', 'POST'])
@login_required
def assign_modules():
    if current_user.role != 'teacher':
        flash("Unauthorized access", "danger")
        return redirect(url_for('core.index'))

    teacher_program_id = current_user.program_id  # Teacher's program
    students = User.query.filter_by(role='student', program_id=teacher_program_id).all()

    # Filter modules to show only those associated with the teacher's program
    teacher_modules = Module.query.filter_by(teacher_id=current_user.id, program_id=teacher_program_id).all()

    if request.method == 'POST':
        if 'assign_module' in request.form:
            student_id = request.form.get('student_id')
            module_id = request.form.get('module_id')
            student = User.query.get(student_id)
            module = Module.query.get(module_id)

            if module not in student.modules:
                student.modules.append(module)
                db.session.commit()
                flash("✅ Module assigned to student!", "success")
            else:
                flash("⚠️ Module already assigned to student.", "warning")

            return redirect(url_for('teacher.teacher_dashboard'))

        elif 'add_module' in request.form:
            name = request.form.get('name')
            description = request.form.get('description')
            credits = request.form.get('credits')
            semester = request.form.get('semester')
            day_of_week = request.form.get('day_of_week')
            time_range = request.form.get('time_range')

            start_hour, end_hour = time_range.split('-')

            # Convert start_time and end_time using the function
            start_time = convert_to_time(start_hour)
            end_time = convert_to_time(end_hour)

            program_code = teacher_program_id  # Ensure that the module is added to the teacher's program
            teacher_email = current_user.email

            # Add new module to the teacher's program
            new_module = Module(
                name=name,
                description=description,
                credits=credits,
                semester=semester,
                day_of_week=day_of_week,
                start_time=start_time,  # Properly formatted start_time
                end_time=end_time,  # Properly formatted end_time
                program_id=program_code,  # Add the teacher's program_id
                teacher_id=current_user.id  # Assign the teacher as the owner
            )

            db.session.add(new_module)
            db.session.commit()

            flash("✅ New module added successfully!", "success")
            return redirect(url_for('teacher.teacher_dashboard'))

    return render_template(
        'assign_modules.html',
        students=students,
        teacher_modules=teacher_modules
    )