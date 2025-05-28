from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from app.models.password_validator import CustomPasswordValidator



class RegistrationForm(FlaskForm):
    email = EmailField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
            Length(max=120, message="Email must be less than 120 characters")
        ],
        render_kw={
            "placeholder": "Enter your email address",
            "class": "form-control",
            "autocomplete": "email"
        }
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, max=20, message="Password must be 8-20 characters long"),
            CustomPasswordValidator()
        ],
        render_kw={
            "placeholder": "Create a password",
            "class": "form-control",
            "autocomplete": "new-password"
        }
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo('password', message="Passwords must match")
        ],
        render_kw={
            "placeholder": "Confirm your password",
            "class": "form-control",
            "autocomplete": "new-password"
        }
    )

    terms_accepted = BooleanField(
        'I agree to the Terms of Service and Privacy Policy',
        validators=[
            DataRequired(message="You must accept the terms and conditions")
        ],
        render_kw={"class": "form-check-input"}
    )

    submit = SubmitField(
        'Create Account',
        render_kw={"class": "btn btn-success w-100"}
    )