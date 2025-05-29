from flask import render_template, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from app import db, User, Car, LoginForm, CarForm, ContactForm, RegistrationForm
from werkzeug.security import check_password_hash
from app import select_where
from app.forms.contact_us import ContactForm
from app.forms.registration_form import RegistrationForm
from datetime import datetime, timedelta
from app.forms.login_form import LoginForm
from app.models import User, Car



# TODO: Create blueprints, etc.
def register_routes(app):

    @app.route('/')
    def home():
        return "Welcome to the app!"  # or render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            user: User = select_where(User.email == form.email.data).one_or_none()

            if user:
                # Check if user is temporarily blocked
                if user.blocked_until and datetime.utcnow() < user.blocked_until:
                    remaining = (user.blocked_until - datetime.utcnow()).seconds
                    flash(f"Account is temporarily blocked. Try again in {remaining} seconds.", "danger")
                    return render_template('login.html', form=form)

                # Validate password
                if user.check_password(form.password.data):
                    login_user(user)
                    user.failed_logins = 0
                    user.blocked_until = None
                    db.session.commit()
                    return redirect(url_for('home'))
                else:
                    user.failed_logins += 1
                    if user.failed_logins >= 3:
                        user.blocked_until = datetime.utcnow() + timedelta(minutes=1)
                        flash("Too many failed attempts. Account is blocked for 1 minute.", "danger")
                    else:
                        flash("Invalid email or password.", "danger")
                    db.session.commit()
            else:
                flash("User not found.", "danger")

        return render_template('login.html', form=form)



    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/cars')
    @login_required
    def car_list():
        cars : list[Car] = Car.query.filter_by(user_id=current_user.id).all()
        return render_template('car_list.html', cars=cars)

    @app.route('/cars/add', methods=['GET', 'POST'])
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
            return redirect(url_for('car_list'))
        return render_template('add_car.html', form=form)

    @app.route('/cars/delete/<int:car_id>', methods=['POST'])
    @login_required
    def delete_car(car_id):
        car = Car.query.get_or_404(car_id)
        if car.user_id != current_user.id:
            return "Unauthorized", 403
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for('car_list'))

    @app.route('/main')
    def main():
        return render_template('main.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            # you could add a function that sends an email or even save it to a database
            flash("Thank you for your message. We'll get back to you soon.", "success")
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/user-menu')
    @login_required
    def user_menu():
        return render_template('user_menu.html')

    @app.route('/image-import-test')
    def image_import_test():
        return render_template('image_import_test.html')

    from app.decorators import role_required

    @app.route('/student-dashboard')
    @role_required('student', 'admin', block_key='student_portal')
    def student_dashboard():
        return "Student dashboard"

    @app.route('/lecturer-dashboard')
    @role_required('lecturer', 'admin', block_key='lecturer_area')
    def lecturer_dashboard():
        return "Lecturer dashboard"

    @app.route('/login/<role>')      # temporary route for testing
    def login_role(role):
        session['role'] = role
        return f"Logged in as {role}"
