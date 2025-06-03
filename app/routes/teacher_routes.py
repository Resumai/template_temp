from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, current_user
from app import db
from app.utils.auth_utils import roles_required


teacher_bp = Blueprint('teacher', __name__)


### Teacher routes ###
@teacher_bp.route('/teacher-dashboard')
@roles_required('teacher')
def teacher_dashboard():
    return render_template('teacher/dashboard.html')