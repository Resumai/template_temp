from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User
# from app.models.car import Car
from db import db
from app.forms.login_form import LoginForm
# from app.forms.car_form import CarForm
# from app.forms.test_form import TestForm

from werkzeug.security import generate_password_hash, check_password_hash


from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import select



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

def register_routes(app):

    @app.route('/')
    def home():
        return "Welcome to the app!"  # or render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = select_where(User.email == form.email.data).one_or_none()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                # For now, redirect to home or something that exists
                return redirect(url_for('home'))  
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
