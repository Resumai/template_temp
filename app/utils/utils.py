
from app import db, User
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