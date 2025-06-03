from flask import render_template, redirect, url_for, flash, Blueprint, request, current_app
from flask_login import login_required, current_user
from app import db
from app.utils.auth_utils import roles_required
from app.utils.utils import delete_photo, get_dashboard_url
from app.forms.forms import ImageUploadForm
import os


### Blueprint Registration ###
bp = Blueprint('core', __name__)


### Core/Unsorted routes ###
@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/user-menu')
@login_required
def user_menu():
    return render_template('user_menu.html')


@bp.route('/upload-profile-picture', methods=['GET', 'POST'])
@login_required
def upload_profile_picture():
    form = ImageUploadForm()
    current_dashboard_url = get_dashboard_url(current_user)

    if form.validate_on_submit():
        # Generate a safe filename based on user ID and MIME
        filename = form.generate_filename()

        
        # Get processed (cropped & resized) image from the form
        image_data = form._processed_image

        # Define where to save the image
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)

        # Save the file
        with open(image_path, 'wb') as f:
            f.write(image_data.read())

        # Optional: Update user's profile picture field
        current_user.profile_picture = filename
        db.session.commit()

        return redirect(current_dashboard_url)

    return render_template(
        'upload_profile_picture.html',
        form=form,
        image=current_user.profile_picture,
        dashboard_url=current_dashboard_url
    )


@bp.route('/delete-profile-picture', methods=['POST'])
@login_required
def delete_profile_picture():
    if current_user.profile_picture:
        delete_photo(current_user)

    current_dashboard_url = get_dashboard_url(current_user)
    return redirect(current_dashboard_url)


