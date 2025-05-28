from flask import Flask, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, User

### MOCK DATA ###
from app.utils.mock_gen import generate_mock_data


### NOT SURE WHAT TO NAME THIS ###
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



### LOGIN LOADER ###
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


### INIT ###
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Hardcoded admin user
        if not User.query.filter_by(email='admin@mail.com').first():
            admin = User(
                name='Admin',
                email='admin@mail.com',
                password_hash=generate_password_hash('password'),
                role='admin',
                program_id=None,   # or assign a valid ID if needed
                group_id=None      # or assign a valid ID if needed
            )

            db.session.add(admin)
            db.session.commit()


        # Mock data generation executions
        generate_mock_data()
    
    app.run(debug=True)