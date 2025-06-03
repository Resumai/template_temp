from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from app import db, Module, Enrollment
from app.utils.auth_utils import roles_required


student_bp = Blueprint('student', __name__)

### Student routes ###
@student_bp.route('/student-dashboard')
@roles_required('student')
def student_dashboard():
    """Display student's dashboard with modules and schedule"""
    try:
        # Get the modules the student is enrolled in
        student_modules = Enrollment.query.filter_by(student_id=current_user.id).all()
        modules = [enrollment.module for enrollment in student_modules]

        if not modules:
            flash("You are not enrolled in any modules. You can add modules below.", "warning")

        # Create a schedule based on the enrolled modules (assuming modules have time information)
        schedule = []
        for module in modules:
            # Assuming 'day_of_week', 'start_time', 'end_time' are in 'Module' and 'teacher' is related
            schedule.append({
                'day_of_week': module.day_of_week,
                'module': module,
                'start_time': module.start_time,
                'end_time': module.end_time,
                'teacher': module.teacher if module.teacher else None
            })

        # Pass the modules and schedule to the template
        return render_template(
            'student/dashboard.html', 
            modules=modules,
            schedule=schedule
        )

    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        print(f"Error loading dashboard: {str(e)}") 
        return redirect(url_for('core.index'))
 


@student_bp.route('/add-module', methods=['GET', 'POST'])
@roles_required('student')
def add_module():
    """Add a module to student's program"""
    try:
        # Fetch available modules based on the student's program
        available_modules = Module.query.filter_by(program_id=current_user.program_id).all()

        if request.method == 'POST':
            module_id = request.form.get('module_id')
            if not module_id:
                flash("Please select a module.", "warning")
                return redirect(url_for('student.add_module'))  # Redirect back if no module is selected

            # Check if the student is already enrolled in the module
            existing_enrollment = Enrollment.query.filter_by(student_id=current_user.id, module_id=module_id).first()
            if existing_enrollment:
                flash("You are already enrolled in this module.", "info")
            else:
                # Enroll the student in the selected module
                new_enrollment = Enrollment(student_id=current_user.id, module_id=module_id)
                db.session.add(new_enrollment)
                db.session.commit()
                flash("Module added successfully!", "success")

            return redirect(url_for('student.student_dashboard'))  # Redirect to dashboard after adding the module

        # If the request is GET, render the add_module page with available modules
        return render_template('add_module.html', available_modules=available_modules)

    except Exception as e:
        flash(f"Error loading available modules: {str(e)}", "danger")
        return redirect(url_for('student.student_dashboard'))  # Redirect to dashboard in case of error
    

@student_bp.route('/enroll_module', methods=['POST'])
def enroll_module():
    try:
        # Jūsų kodas čia, pavyzdžiui, užregistruoti modulį studentui
        module_id = request.form['module_id']
        student_id = current_user.id

        # Pavyzdys, kaip sukurti užrašą (enrollment)
        enrollment = Enrollment(student_id=student_id, module_id=module_id)
        db.session.add(enrollment)
        db.session.commit()

        flash("Module enrolled successfully!", "success")
        return redirect(url_for('student.student_dashboard'))

    except Exception as e:
        flash(f"Error enrolling in module: {str(e)}", "danger")
        return redirect(url_for('student.student_dashboard'))  # Redirect to dashboard on error


@student_bp.route('/delete-module/<int:module_id>', methods=['POST'])
@roles_required('student')
def delete_module(module_id):
    """ Delete student's enrolled module """
    try:
        # Find the student's enrollment in the module
        enrollment = Enrollment.query.filter_by(student_id=current_user.id, module_id=module_id).first()

        if not enrollment:
            flash("You are not enrolled in this module.", "warning")
            return redirect(url_for('student.student_dashboard'))

        # Delete the enrollment
        db.session.delete(enrollment)
        db.session.commit()
        flash("Module deleted successfully!", "success")

        return redirect(url_for('student.student_dashboard'))  # Redirect to the dashboard after deleting the module

    except Exception as e:
        flash(f"Error deleting module: {str(e)}", "danger")
        return redirect(url_for('student.student_dashboard'))