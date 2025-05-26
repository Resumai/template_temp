from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import select, table

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

### MODELS ###





class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer)
    color = db.Column(db.String(32))
    vin = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

### FORMS ###
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year')
    color = StringField('Color')
    vin = StringField('VIN')
    submit = SubmitField('Save')

class TestForm(FlaskForm):
    submit = SubmitField('Test select_where')


# class SelectWrapper:
#     def __init__(self, model_class, *expressions):
#         self.model_class = model_class
#         self.expressions = expressions

#     def statement(self):
#         return select(self.model_class).where(*self.expressions)

#     def one_or_none(self):
#         return db.session.execute(self.statement()).scalar_one_or_none()

#     def all(self):
#         return db.session.execute(self.statement()).scalars().all()

#     def first(self):
#         return db.session.execute(self.statement()).scalars().first()

#     def count(self):
#         return len(self.all())  # Simplified for now


# def select_where(*expressions):
#     model = expressions[0].left.class_ # means, model_class is classes that use db.Model
#     return SelectWrapper(model, *expressions)


from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql.schema import Table
from sqlalchemy import inspect

def select_where(expression : BinaryExpression):
    column = expression.left
    model = column._annotations['parententity']

    # for mapper in db.Model.registry.mappers:
    # if mapper.class_.__table__ is table:
    #     model = mapper.class_
    #     break


    print("column:", type(model))
    print("column dir:", dir(model))
    stmt = select(model).where(expression)
    # db.session.get(model, expression.right)
    # print("stmt:\n", stmt)
    return db.session.execute(stmt).scalar_one_or_none()
    # return

# def select_where(column, value):
#     model = column.class_
#     print("model:\n", model)
#     stmt = select(model).where(column == value)
#     print("stmt:\n", stmt)
#     return db.session.execute(stmt).scalar_one_or_none()


@app.route('/', methods=['GET', 'POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        # user = select_where(User.email == form.email.data).one_or_none()
        # selection = select(User.email).where(email == form.email.data)
        # user = db.session.execute(selection).scalar_one_or_none()
        # user = select_where(User.email, "test@example.com")
        user = select_where(User.email == "test@example.com")
        print("user data after execute\n:", dir(user))
        print("user data after execute email\n:", dir(user.email))
        # user = User.query.filter_by(email="test@example.com").first()
        # print("user\n:", user)
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
        # user = select_where(User.email == form.email.data).one_or_none()
        user = select_where(User.email == form.email.data)
        # selection = select(User.email).where(email == form.email.data)
        # user = db.session.execute(selection).scalar_one_or_none()
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
        car = Car(**form.data, user_id=current_user.id)
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
        # Create a dummy user for testing if none exists
        if not User.query.filter_by(email='test@example.com').first():
            user = User(email='test@example.com', password_hash=generate_password_hash('123'))
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)
