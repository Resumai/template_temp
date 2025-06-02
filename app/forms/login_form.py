from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    email = StringField(
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
            Length(min=8, message="Password must be at least 8 characters long")
        ],
        render_kw={
            "placeholder": "Enter your password",
            "class": "form-control",
            "autocomplete": "current-password"
        }
    )
    
    remember_me = BooleanField(
        'Remember Me',
        render_kw={"class": "form-check-input"}
    )
    
    submit = SubmitField(
        'Login',
        render_kw={"class": "btn btn-primary"}
    )
    
    def validate_email(self, email):
        """Custom validation for email field"""
        # add custom email validation logic here
        # For example, checking against a blacklist or specific domain requirements
        pass
    
    def validate_password(self, password):
        """Custom validation for password field"""
        # You can add custom password validation logic here
        # For example, checking password complexity
        pass
