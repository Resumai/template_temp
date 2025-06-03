from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, DateField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, NumberRange, Length
from werkzeug.utils import secure_filename
from flask_login import current_user

import io
from PIL import Image, UnidentifiedImageError
import os
from flask import flash
from app import db
from app.models.user import User



class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=3, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=15)])
    date_of_birth = DateField('Date of Birth')
    major = StringField('Major', validators=[DataRequired(), Length(min=2, max=100)])
    year = SelectField('Year', choices=[('1', 'Year 1'), ('2', 'Year 2'), ('3', 'Year 3'), ('4', 'Year 4')], coerce=int)
    gpa = FloatField('GPA', validators=[NumberRange(min=0.0, max=4.0)])
    address = TextAreaField('Address')
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Graduated', 'Graduated')])


class FacultyForm(FlaskForm):
    employee_id = StringField('Employee ID', validators=[DataRequired(), Length(min=3, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=15)])
    department = StringField('Department', validators=[DataRequired(), Length(min=2, max=100)])
    position = SelectField('Position', choices=[
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Lecturer', 'Lecturer'),
        ('Adjunct', 'Adjunct')
    ])
    salary = FloatField('Salary', validators=[NumberRange(min=0)])
    hire_date = DateField('Hire Date')
    office_location = StringField('Office Location', validators=[Length(max=100)])
    specialization = StringField('Specialization', validators=[Length(max=200)])


class CourseForm(FlaskForm):
    code = StringField('Course Code', validators=[DataRequired(), Length(min=3, max=20)])
    name = StringField('Course Name', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description')
    credits = IntegerField('Credits', validators=[DataRequired(), NumberRange(min=1, max=6)])
    department = StringField('Department', validators=[DataRequired(), Length(min=2, max=100)])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1, max=500)])
    semester = SelectField('Semester', choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2020, max=2030)])
    schedule = StringField('Schedule', validators=[Length(max=100)])
    room = StringField('Room', validators=[Length(max=50)])
    prerequisites = StringField('Prerequisites', validators=[Length(max=200)])
    instructor_id = SelectField('Instructor', coerce=int)

class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    semester = SelectField('Semester', choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2020, max=2030)])
    grade = SelectField('Grade', choices=[
        ('', 'No Grade'),
        ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'), ('D+', 'D+'), ('D', 'D'), ('F', 'F')
    ])
    status = SelectField('Status', choices=[
        ('Enrolled', 'Enrolled'),
        ('Completed', 'Completed'),
        ('Dropped', 'Dropped'),
        ('Withdrawn', 'Withdrawn')
    ])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
MAX_DIMENSION = 512  # Max width/height

# TODO: probably need to check for file size too i assume... profile pictures should be 10kx10k resolution or smth
class ImageUploadForm(FlaskForm):
    image = FileField('Choose picture', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, 'Only .jpg, .jpeg, or .png files are allowed.')
    ])
    submit = SubmitField('Upload Image')

    def validate_image(form, field):
        file = field.data
        if file:
            if file.mimetype not in ALLOWED_MIME_TYPES:
                raise ValidationError('Invalid file MIME type. Only JPEG and PNG are allowed.')
            file.seek(0, os.SEEK_END)
            if file.tell() > MAX_FILE_SIZE:
                raise ValidationError('File too large. Maximum size is 2MB.')
            file.seek(0)

    def generate_filename(self) -> str:
        file = self.image.data
        ext = {
            'image/jpeg': 'jpg',
            'image/png': 'png'
        }.get(file.mimetype)
        if not ext:
            raise ValueError("Unsupported MIME type.")
        return secure_filename(f"uid_{current_user.id}_pic.{ext}")

def image_upload(form: ImageUploadForm, user: User):
    
    file = form.image.data
    filename = form.generate_filename()

    try:
        file_stream = io.BytesIO(file.read())
        image = Image.open(file_stream)
        image.verify()
        file_stream.seek(0)
        image = Image.open(file_stream)

        if image.width > MAX_DIMENSION or image.height > MAX_DIMENSION:
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

        relative_path = f"uploads/{filename}"
        full_path = os.path.join('app/static', relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        image.save(full_path)

        user.profile_picture = relative_path
        db.session.commit()
        flash("Profile picture uploaded successfully!", "success")

    except UnidentifiedImageError:
        flash("Upload failed: the file is not a valid image.", "danger")
    except OSError as e:
        flash("Error saving the image file.", "danger")
        print("OSError:", e)
    except ValueError as e:
        flash("Image processing failed: invalid content.", "danger")
        print("ValueError:", e)
    except Exception as e:
        flash("Unexpected error occurred during upload.", "danger")
        print("Unexpected error:", e)



