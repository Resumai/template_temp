from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from app import db, User, LoginForm, RegistrationForm, StudyProgram
# from app.models import User, StudyProgram
from flask_bcrypt import check_password_hash, generate_password_hash
from app.utils.curd_utils import select_where
from app.utils.group_utils import get_or_create_group
from datetime import datetime, timedelta



auth_bp = Blueprint('auth', __name__)


### Auth related routes ###
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user : User = select_where(User.email == form.email.data).one_or_none()
        if user.is_temporarily_blocked():
            reason = user.block_reason or "your account is temporarily blocked"
            flash(f"{reason} until {user.blocked_until.strftime('%H:%M:%S')}.", "danger")
            return render_template('auth/login.html', form=form)

        elif user and check_password_hash(user.password_hash, form.password.data):
            user.failed_logins = 0  # Reset on success
            user.block_reason = None
            db.session.commit()
            login_user(user)

            if user.role == 'admin':
                flash("Welcome back, Admin!", "success")
                return redirect(url_for('core.admin_dashboard'))
            elif user.role == 'teacher':
                flash("Welcome back, Teacher!", "success")
                return redirect(url_for('core.teacher_dashboard'))
            elif user.role == 'student':
                flash("Welcome back, Student!", "success")
                return redirect(url_for('student.student_dashboard'))
            else:
                flash("Unknown role. Please contact support.", "danger")
                return redirect(url_for('auth.login'))     
        else:
            user.failed_logins += 1
            if user.failed_logins >= 3:
                user.blocked_until = datetime.utcnow() + timedelta(minutes=5)
                user.failed_logins = 0  # Optionally reset
                flash("Too many failed attempts. You are blocked for 5 minutes.", "danger")
            else:
                flash("Invalid credentials.", "warning")
            db.session.commit()
            return render_template('auth/login.html', form=form)

    flash("User not found.", "danger")
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