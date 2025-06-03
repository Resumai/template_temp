from app.extensions import db


# from app.models.student import Student

# Models
from app.models import Faculty
from app.models import StudentGroup
from app.models import StudyProgram
from app.models import User


from app.models import Module
from app.models import Enrollment
from app.models import Assessment


# Model for testing
from app.models import Car

# Forms
from app.forms.login_form import LoginForm
from app.forms.registration_form import RegistrationForm
from app.forms.forms import StudentForm, FacultyForm
from app.forms.contact_us import ContactForm

# Form for testing
from app.forms.car_form import CarForm

# Utils
from app.utils.curd_utils import select_where
from app.utils.data_ops import create_admin_user
from app.utils.mock_gen import generate_mock_data

