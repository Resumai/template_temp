from app import db, User
from flask_bcrypt import generate_password_hash


def create_admin_user():
    if not User.query.filter_by(email='admin@mail.com').first():
        admin = User(
            name='Admin',
            email='admin@mail.com',
            password_hash=generate_password_hash('password'),
            role='admin',
            program_id=None,
            group_id=None
        )
        db.session.add(admin)
        db.session.commit()