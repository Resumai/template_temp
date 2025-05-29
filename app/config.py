from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# 

BLOCKED_FEATURES = {
    'student_portal': False,
    'lecturer_area': True,  # Blocked for now
}
