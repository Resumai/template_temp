from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from db import db

# Models
from app.models.user import User
from app.models.car import Car
#Forms
from app.forms.login_form import LoginForm
from app.forms.car_form import CarForm
from app.forms.test_form import TestForm

# Type Checking
from sqlalchemy.sql.elements import BinaryExpression


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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


@app.route('/', methods=['GET', 'POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        user = select_where(User.email == "test@example.com").one_or_none()
        if user:
            login_user(user)
            flash("User logged in successfully")
            return redirect(url_for('test'))
        else:
            flash("User not found")
            return redirect(url_for('test'))
    return render_template('test.html', form=form)

### LOGIN LOADER ###
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

### ROUTES ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # selection = select(User.email).where(email == form.email.data)
        # user = db.session.execute(selection).scalar_one_or_none()
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
    # if form.validate_on_submit():
    #     car = Car(**form.data, user_id=current_user.id)
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

### INIT ###
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a admin user for testing if none exists - admin rights not yet implemented
        if not User.query.filter_by(email ='admin@mail.com').first():
            user = User(username='Admin', email ='admin@mail.com', password_hash = generate_password_hash('pass'))
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)
