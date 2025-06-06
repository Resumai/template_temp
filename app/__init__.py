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
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import ContactForm
from app.forms import ImageUploadForm

# Form for testing
from app.forms import CarForm

# Utils
from app.utils.data_ops import create_admin_user
from app.utils.mock_gen import generate_mock_data

