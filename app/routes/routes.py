from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User
from app.models.car import Car
from db import db
from app.forms.login_form import LoginForm
from app.forms.car_form import CarForm
from app.forms.contact_us import ContactForm
from app.forms.registration_form import RegistrationForm

# from app.forms.test_form import TestForm

from werkzeug.security import generate_password_hash, check_password_hash


from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import select


# TODO: move to utils or smth
class SelectWrapper:
    def __init__(self, model_class, *expressions):
        self.model_class = model_class
        self.expressions = expressions

    def statement(self):
        return select(self.model_class).where(*self.expressions)

    def one_or_none(self):
        return db.session.execute(self.statement()).scalar_one_or_none()

    def all(self):
        return db.session.execute(self.statement()).scalars().all()

    def first(self):
        return db.session.execute(self.statement()).scalars().first()

    def count(self):
        return len(self.all())




def select_where(*expressions : BinaryExpression):
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo
    return SelectWrapper(model, *expressions)

# app/routes/routes.py

# TODO: Create blueprints, etc.
def register_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = select_where(User.email == form.email.data).one_or_none()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('car_list'))
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/cars')
    @login_required
    def car_list():
        cars = Car.query.filter_by(user_id=current_user.id).all()
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
    
    @app.route('/')
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
        # Normally, you'd send an email or save the message to a database
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