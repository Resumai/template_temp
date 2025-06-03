from flask import flash, url_for
from app import db
from app.models import User
from app.forms.forms import ImageUploadForm  
from werkzeug.utils import secure_filename
import os


# Helper function to upload profile picture.
# For user probably best to just use current_user
def image_upload(form : ImageUploadForm, user : User):
    filename = form.generate_filename()
    relative_path = f"uploads/{filename}" 

    # Translates to full path: app/static/uploads/{filename}
    full_path = os.path.join('app/static', relative_path) 
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    form.image.data.save(full_path)

    user.profile_picture = relative_path
    db.session.commit()


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
