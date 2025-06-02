from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from app import db
from app.utils.auth_utils import roles_required
from app.utils.utils import image_upload, delete_photo, get_dashboard_url
from app.forms.forms import ImageUploadForm  


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
        image_upload(form, current_user)

        return redirect(current_dashboard_url)

    return render_template('/upload_profile_picture.html', form=form, image=current_user.profile_picture, dashboard_url=current_dashboard_url)


@bp.route('/delete-profile-picture', methods=['POST'])
@login_required
def delete_profile_picture():
    if current_user.profile_picture:
        delete_photo(current_user)

    current_dashboard_url = get_dashboard_url(current_user)
    return redirect(current_dashboard_url)


