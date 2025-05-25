from typing import Type
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt


# For easier type checking
from sqlalchemy import Column, Integer,  String, select, update, delete, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from sqlalchemy.orm import InstrumentedAttribute, DeclarativeMeta
    from sqlalchemy import BinaryExpression



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

### MODELS ###

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
        return len(self.all())  # Simplified for now







class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    cars = relationship('Car', backref='owner', lazy=True)


class Car(db.Model):
    id = Column(Integer, primary_key=True)
    make = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    year = Column(Integer)
    color = Column(String(32))
    vin = Column(String(128))
    created_at = Column(DateTime, default=dt.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

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




# def find_by_column(column : InstrumentedAttribute, value):
#     model = column.class_
#     statement = select(model).where(column == value)
#     return db.session.execute(statement).scalar_one_or_none()
    


def select_where(*expressions : BinaryExpression):
    left_side : InstrumentedAttribute = expressions[0].left # left side of the expression
    model_class : DeclarativeMeta = left_side.class_ # means, model_class is classes that use db.Model
    return SelectWrapper(model_class, *expressions)

# user = select_where(User.email == "test@example.com").one_or_none()
# print(user)


# def update_where(model, values: dict, *expressions: BinaryExpression) -> ExecuteWrapper:
#     statement = update(model).where(*expressions).values(**values)
#     return ExecuteWrapper(statement)

# def delete_where(expression: BinaryExpression):
#     value = expression.right
#     column = expression.left
#     model = column.class_

#     if not column.primary_key:
#         raise ValueError(f"delete_where only supports primary key deletion. Got: {column}")

#     obj = db.session.get(model, value)
#     if obj:
#         db.session.delete(obj)
#         db.session.commit()



def delete_where(*expressions: BinaryExpression):
    model: DeclarativeMeta = expressions[0].left.class_
    statement = select(model).where(*expressions)
    results = db.session.execute(statement).scalars().all()

    for obj in results:
        db.session.delete(obj)

    db.session.commit()



delete_where(User.id == 1)

# user = find_by_column(User.email == 'test@example.com')

# T = TypeVar('T')
# def find_by_column(expression : BinaryExpression) -> T | None:
#     """Find a single object by a column expression."""
#     left_side : InstrumentedAttribute = expression.left
#     model_class : DeclarativeMeta = left_side.class_ # means, model_class is classes that use db.Model
#     statement = select(model_class).where(expression)
#     result = db.session.execute(statement).scalar_one_or_none()
#     return cast(T | None, result) # cast() helps type checker understand that result can be T or None




### LOGIN LOADER ###
@login_manager.user_loader
def load_user(user_id):
    # return User.query.get(int(user_id))
    return db.session.get(User, int(user_id))

### ROUTES ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        user : User | None = find_by_column(User.email == form.email.data)
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
    # cars = Car.query.filter_by(user_id=current_user.id).all()
    cars = find_by_column(Car.user_id == current_user.id)
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
