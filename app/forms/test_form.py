from flask_wtf import FlaskForm
from wtforms import SubmitField

class TestForm(FlaskForm):
    submit = SubmitField('Test select_where')