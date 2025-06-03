from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from app import db
from app.utils.auth_utils import roles_required


admin_bp = Blueprint('admin', __name__)


### Admin routes ###
@admin_bp.route('/admin-dashboard')
@roles_required('admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')