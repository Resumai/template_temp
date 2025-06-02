from flask import Flask
from flask_login import LoginManager
from app import db, User, create_admin_user, generate_mock_data
from app.routes.routes import bp, car_bp, auth_bp, info_bp
import logging


### FLASK SET-UP ###
app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
    )
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

### LOGGER SETUP ###
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


### LOGIN LOADER ###
@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception as e:
        app.logger.error(f"Error loading user {user_id}: {e}")
        return None
    return db.session.get(User, int(user_id))


### INIT ###
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created.")
        except Exception as e:
            logger.error(f"database initialization failed: {e}")

        try:
            create_admin_user()
            logger.info("Admin user created.")
        except Exception as e:
            logger.error(f"Adimin user creation failed: {e}")

        # Hardcoded admin user
        try:
            generate_mock_data()
            logger.info("Mock data generated.")
        except Exception as e:
            logger.error(f"Mock data generation failed: {e}")

        try:
            app.run(debug=True)
        except Exception as e:
            app.logger.error(f"Error starting the app: {e}")
        print("App started successfully.")