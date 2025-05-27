from flask import Flask, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

# Models
from app.models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


### ROUTES ###
from app.routes.routes import register_routes
register_routes(app)

### TEST ROUTE ###
# @app.route('/', methods=['GET', 'POST'])
# def test():
#     form = TestForm()
#     if form.validate_on_submit():
#         user = select_where(User.email == "test@example.com").one_or_none()
#         if user:
#             login_user(user)
#             flash("User logged in successfully")
#             return redirect(url_for('test'))
#         else:
#             flash("User not found")
#             return redirect(url_for('test'))
#     return render_template('test.html', form=form)




### LOGIN LOADER ###
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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
