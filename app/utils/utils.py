from flask import flash, url_for
from app import db, User
from app.forms.forms import ImageUploadForm  
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import os


def delete_photo(user: User):
    try:
        filepath = os.path.join('app/static', user.profile_picture)
        if os.path.exists(filepath):
            os.remove(filepath)

        user.profile_picture = None
        db.session.commit()
        flash("Profile picture deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting profile picture: {str(e)}", "danger")


def get_dashboard_url(user):
    if user.role == 'admin':
        return url_for('core.admin_dashboard')
    elif user.role == 'student':
        return url_for('student.student_dashboard')
    elif user.role == 'teacher':
        return url_for('core.teacher_dashboard')
    return url_for('core.index')  # fallback
