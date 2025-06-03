from flask import render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from app import db, Car, CarForm



car_bp = Blueprint('car', __name__)



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