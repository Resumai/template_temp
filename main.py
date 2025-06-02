from flask import Flask
from flask_login import LoginManager
from app import db, User, create_admin_user, generate_mock_data
from app.routes.routes import bp, car_bp, auth_bp, info_bp, student_bp


### FLASK SET-UP ###
app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
    )
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

### INIT DB ###
db.init_app(app)

### LOGIN MANAGER ###
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


### ROUTES ###
app.register_blueprint(bp, url_prefix='/')
app.register_blueprint(car_bp, url_prefix='/car')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(info_bp, url_prefix='/info')
app.register_blueprint(student_bp, url_prefix='/student')


### LOGIN LOADER ###
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


### INIT ###
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Hardcoded admin user
        create_admin_user()

        # Mock data generation execution
        generate_mock_data()

    app.run(debug=True)