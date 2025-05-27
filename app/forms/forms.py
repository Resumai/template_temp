from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, NumberRange, Length


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