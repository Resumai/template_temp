# app/utils/login_utils.py

from flask import flash, redirect, url_for, render_template
from flask_login import login_user
from app import db
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

def handle_failed_login(user):
    user.failed_logins += 1
    if user.failed_logins >= 3:
        user.blocked_until = datetime.utcnow() + timedelta(minutes=5)
        user.failed_logins = 0
        flash("Too many failed attempts. You are blocked for 5 minutes.", "danger")
    else:
        flash("Invalid credentials.", "warning")
    db.session.commit()
    return render_template("auth/login.html")


def handle_successful_login(user):
    user.failed_logins = 0
    user.block_reason = None
    db.session.commit()
    login_user(user)

    if user.role == 'admin':
        flash("Welcome back, Admin!", "success")
        return redirect(url_for("core.admin_dashboard"))
    elif user.role == 'teacher':
        flash("Welcome back, Teacher!", "success")
        return redirect(url_for("core.teacher_dashboard"))
    elif user.role == 'student':
        flash("Welcome back, Student!", "success")
        return redirect(url_for("core.student_dashboard"))
    else:
        flash("Unknown role. Please contact support.", "danger")
        return render_template("auth/login.html")
