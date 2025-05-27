from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app import db, User, Car, LoginForm, CarForm
from werkzeug.security import check_password_hash
from app import select_where


# TODO: Create blueprints, etc.
def register_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user : User = select_where(User.email == form.email.data).one_or_none()
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