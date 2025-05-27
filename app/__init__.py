from app.extensions import db



# Models
from app.models.user import User
from app.models.student import Student



# Forms
from app.forms.login_form import LoginForm
from app.forms.registration_form import RegistrationForm
from app.forms.forms import StudentForm, FacultyForm
from app.forms.contact_us import ContactForm

# Utils
from app.utils.utils import select_where



# For Testing
from app.models.car import Car
from app.forms.car_form import CarForm