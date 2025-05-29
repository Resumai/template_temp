from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db, User, Car, LoginForm, CarForm, ContactForm, RegistrationForm
from werkzeug.security import check_password_hash
from app import select_where
from app.forms.contact_us import ContactForm
from app.forms.registration_form import RegistrationForm


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
    
    @app.route('/image-import-test', methods=['GET', 'POST'])
    @login_required
    def image_import_test():
        from app.forms.forms import ImageUploadForm  
        from werkzeug.utils import secure_filename
        import os

        form = ImageUploadForm()
        if form.validate_on_submit():
            image = form.image.data
            filename = secure_filename(f"{current_user.id}_{image.filename}")
            relative_path = f"uploads/{filename}"  # ✅ tik nuo "static/"
            full_path = os.path.join('static', relative_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            image.save(full_path)

            current_user.profile_picture = relative_path
            db.session.commit()

            flash("Paveikslėlis įkeltas sėkmingai!", "success")
            return redirect(url_for('image_import_test'))

        return render_template('image_import_test.html', form=form, image=current_user.profile_picture)
