from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from app import db, User, Car, LoginForm, CarForm, ContactForm, RegistrationForm, StudentGroup, StudyProgram, Module, Assessment, Enrollment
from flask_bcrypt import check_password_hash, generate_password_hash
from app.utils.curd_utils import select_where
from app.utils.group_utils import get_or_create_group
from app.utils.auth_utils import roles_required
from app.utils.utils import image_upload, delete_photo
from datetime import datetime

# New imports
from app.forms.forms import ImageUploadForm  



### Blueprint Registration ###
bp = Blueprint('core', __name__)
auth_bp = Blueprint('auth', __name__)
car_bp = Blueprint('car', __name__)
info_bp = Blueprint('info', __name__)
student_bp = Blueprint('student', __name__)


### Auth related routes ###
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user : User = select_where(User.email == form.email.data).one_or_none()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)

            if user.role == 'admin':
                flash("Welcome back, Admin!", "success")
                return redirect(url_for('core.admin_dashboard'))
            elif user.role == 'teacher':
                flash("Welcome back, Teacher!", "success")
                return redirect(url_for('core.teacher_dashboard'))
            elif user.role == 'student':
                flash("Welcome back, Student!", "success")
                return redirect(url_for('core.student_dashboard'))
            else:
                flash("Unknown role. Please contact support.", "danger")
                return redirect(url_for('login'))
            
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.program.choices = [(str(p.id), p.name) for p in StudyProgram.query.all()]
    if form.validate_on_submit():
        selected_program = StudyProgram.query.get(int(form.program.data))
        role = form.role.data
        email = form.email.data
        password = form.password.data

        group = get_or_create_group(selected_program)
        
        user = User(
            name=form.name.data,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            program=selected_program,
            group=group
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


### Car related routes ###
@car_bp.route('/cars')
@login_required
def car_list():
    cars : list[Car] = Car.query.filter_by(user_id=current_user.id).all()
    return render_template('car_stuff/car_list.html', cars=cars)

@car_bp.route('/cars/add', methods=['GET', 'POST'])
@login_required
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            color=form.color.data,
            vin=form.vin.data,
            user_id=current_user.id
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('car.car_list'))
    return render_template('car_stuff/add_car.html', form=form)

@car_bp.route('/cars/delete/<int:car_id>', methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        return "Unauthorized", 403
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('car.car_list'))


### Info routes ###
@info_bp.route('/privacy')
def privacy():
    return render_template('info/privacy.html')

@info_bp.route('/terms')
def terms():
    return render_template('info/terms.html')

@info_bp.route('/contact', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
    # Normally, you'd send an email or save the message to a database
        flash("Thank you for your message. We'll get back to you soon.", "success")
        return redirect(url_for('core.contact_us'))
    return render_template('info/contact_us.html', form=form)


### Core/Unsorted routes ###
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/user-menu')
@login_required
def user_menu():
    return render_template('user_menu.html')

@bp.route('/admin-dashboard')
@roles_required('admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/teacher-dashboard')
@roles_required('teacher')
def teacher_dashboard():
    return render_template('teacher/dashboard.html')

@bp.route('/student-dashboard')
@roles_required('student')
def student_dashboard():
    return render_template('student/dashboard.html')

# TODO: Refactor further for easier use
@bp.route('/upload-profile-picture', methods=['GET', 'POST'])
@login_required
def upload_profile_picture():
    form = ImageUploadForm()
    if form.validate_on_submit():
        image_upload(form, current_user)
        return redirect(url_for('core.upload_profile_picture'))

    return render_template('/upload_profile_picture.html', form=form, image=current_user.profile_picture)



@bp.route('/delete-profile-picture', methods=['POST'])
@login_required
def delete_profile_picture():
    if current_user.profile_picture:
        delete_photo(current_user)
    return redirect(url_for('core.' + current_user.role + '_dashboard'))



# Create student blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@roles_required('student')
def dashboard():
    """Student dashboard showing enrolled modules and upcoming assessments"""
    try:
        # Get student's enrolled modules
        enrolled_modules = db.session.query(Module).join(Enrollment).filter(
            Enrollment.student_id == current_user.id
        ).all()
        
        
        # Get upcoming assessments for enrolled modules
        upcoming_assessments = db.session.query(Assessment).join(Module).join(Enrollment).filter(
            Enrollment.student_id == current_user.id,
            Assessment.date >= datetime.now()
        ).order_by(Assessment.date).limit(5).all()
        
        # Get student's grades
        grades = db.session.query(Enrollment).filter(
            Enrollment.student_id == current_user.id,
            Enrollment.grade.isnot(None)
        ).all()
        
        return render_template('student/dashboard.html', 
                             enrolled_modules=enrolled_modules,
                             upcoming_assessments=upcoming_assessments,
                             grades=grades)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        return render_template('student/dashboard.html', 
                             enrolled_modules=[],
                             upcoming_assessments=[],
                             grades=[])

@student_bp.route('/modules')
@roles_required('student')
def view_modules():
    """View all available modules for student's program"""
    try:
        if not current_user.program_id:
            flash("You are not assigned to any study program. Please contact administration.", "warning")
            return redirect(url_for('student.dashboard'))
        
        # Get all modules for student's program
        available_modules = Module.query.filter_by(program_id=current_user.program_id).all()
        
        # Get modules student is already enrolled in
        enrolled_module_ids = db.session.query(Enrollment.module_id).filter_by(
            student_id=current_user.id
        ).all()
        enrolled_module_ids = [id[0] for id in enrolled_module_ids]
        
        return render_template('student/modules.html', 
                             available_modules=available_modules,
                             enrolled_module_ids=enrolled_module_ids)
    except Exception as e:
        flash(f"Error loading modules: {str(e)}", "danger")
        return render_template('student/modules.html', 
                             available_modules=[],
                             enrolled_module_ids=[])

@student_bp.route('/enroll/<int:module_id>')
@roles_required('student')
def enroll_module(module_id):
    """Enroll student in a module"""
    try:
        module = Module.query.get_or_404(module_id)
        
        # Check if module belongs to student's program
        if module.program_id != current_user.program_id:
            flash("You cannot enroll in modules from other programs.", "danger")
            return redirect(url_for('student.view_modules'))
        
        # Check if already enrolled
        existing_enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            module_id=module_id
        ).first()
        
        if existing_enrollment:
            flash("You are already enrolled in this module.", "warning")
            return redirect(url_for('student.view_modules'))
        
        # Check prerequisites
        if module.prerequisites:
            student_completed_modules = db.session.query(Enrollment.module_id).filter_by(
                student_id=current_user.id
            ).filter(Enrollment.grade >= 5.0).all()  # Assuming 5.0 is passing grade
            completed_ids = [id[0] for id in student_completed_modules]
            
            for prereq in module.prerequisites:
                if prereq.id not in completed_ids:
                    flash(f"You must complete '{prereq.name}' before enrolling in this module.", "danger")
                    return redirect(url_for('student.view_modules'))
        
        # Create enrollment
        enrollment = Enrollment(
            student_id=current_user.id,
            module_id=module_id
        )
        db.session.add(enrollment)
        db.session.commit()
        
        flash(f"Successfully enrolled in '{module.name}'!", "success")
        return redirect(url_for('student.view_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error enrolling in module: {str(e)}", "danger")
        return redirect(url_for('student.view_modules'))

@student_bp.route('/unenroll/<int:module_id>')
@roles_required('student')
def unenroll_module(module_id):
    """Unenroll student from a module"""
    try:
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            module_id=module_id
        ).first()
        
        if not enrollment:
            flash("You are not enrolled in this module.", "warning")
            return redirect(url_for('student.view_modules'))
        
        # Check if module has already been graded
        if enrollment.grade is not None:
            flash("Cannot unenroll from a module that has already been graded.", "danger")
            return redirect(url_for('student.view_modules'))
        
        module_name = enrollment.module.name
        db.session.delete(enrollment)
        db.session.commit()
        
        flash(f"Successfully unenrolled from '{module_name}'.", "success")
        return redirect(url_for('student.view_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error unenrolling from module: {str(e)}", "danger")
        return redirect(url_for('student.view_modules'))

@student_bp.route('/schedule')
@roles_required('student')
def view_schedule():
    """View student's personal schedule"""
    try:
        # Get enrolled modules with their schedules
        enrolled_modules = db.session.query(Module).join(Enrollment).filter(
            Enrollment.student_id == current_user.id
        ).all()
        
        # Get upcoming assessments
        upcoming_assessments = db.session.query(Assessment).join(Module).join(Enrollment).filter(
            Enrollment.student_id == current_user.id,
            Assessment.date >= datetime.now()
        ).order_by(Assessment.date).all()
        
        return render_template('student/schedule.html', 
                             enrolled_modules=enrolled_modules,
                             upcoming_assessments=upcoming_assessments)
    except Exception as e:
        flash(f"Error loading schedule: {str(e)}", "danger")
        return render_template('student/schedule.html', 
                             enrolled_modules=[],
                             upcoming_assessments=[])

@student_bp.route('/grades')
@roles_required('student')
def view_grades():
    """View student's grades"""
    try:
        # Get all enrollments with grades
        enrollments_with_grades = db.session.query(Enrollment).filter(
            Enrollment.student_id == current_user.id,
            Enrollment.grade.isnot(None)
        ).all()
        
        # Calculate GPA
        total_credits = 0
        total_grade_points = 0
        
        for enrollment in enrollments_with_grades:
            if enrollment.module and enrollment.grade:
                credits = enrollment.module.credits
                total_credits += credits
                total_grade_points += (enrollment.grade * credits)
        
        gpa = round(total_grade_points / total_credits, 2) if total_credits > 0 else 0
        
        return render_template('student/grades.html', 
                             enrollments=enrollments_with_grades,
                             gpa=gpa,
                             total_credits=total_credits)
    except Exception as e:
        flash(f"Error loading grades: {str(e)}", "danger")
        return render_template('student/grades.html', 
                             enrollments=[],
                             gpa=0,
                             total_credits=0)

@student_bp.route('/profile')
@roles_required('student')
def view_profile():
    """View student profile information"""
    try:
        return render_template('student/profile.html', user=current_user)
    except Exception as e:
        flash(f"Error loading profile: {str(e)}", "danger")
        return render_template('student/profile.html', user=current_user)