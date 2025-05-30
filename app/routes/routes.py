from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from app import db, User, Car, LoginForm, CarForm, ContactForm, RegistrationForm, StudentGroup, StudyProgram
from flask_bcrypt import check_password_hash, generate_password_hash
from app import select_where
from app.utils.group_utils import get_or_create_group
from app.utils.auth_utils import roles_required
from app.utils.utils import image_upload

# New imports
from app.forms.forms import ImageUploadForm  
from werkzeug.utils import secure_filename
import os



### Blueprint Registration ###
bp = Blueprint('core', __name__)
auth_bp = Blueprint('auth', __name__)
car_bp = Blueprint('car', __name__)
info_bp = Blueprint('info', __name__)


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
        return redirect(url_for('core.image_import_test'))

    return render_template('/upload_profile_picture.html', form=form, image=current_user.profile_picture)


from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import os

@bp.route('/delete-profile-picture', methods=['POST'])
@login_required
def delete_profile_picture():
    if current_user.profile_picture:
        # Pašaliname nuotrauką iš serverio
        try:
            os.remove(os.path.join('app/static', current_user.profile_picture))
            # Išvalome naudotojo profilio nuotrauką iš duomenų bazės
            current_user.profile_picture = None
            db.session.commit()
            flash("Profile picture deleted successfully!", "success")
        except Exception as e:
            flash(f"Error deleting profile picture: {str(e)}", "danger")
    
    return redirect(url_for('core.' + current_user.role + '_dashboard'))
