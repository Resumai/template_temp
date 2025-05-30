from app import db, User
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import select

from app.forms.forms import ImageUploadForm  
from werkzeug.utils import secure_filename
import os


# TODO: Move to db_utils or smth that is more db-only related
class SelectWrapper:
    def __init__(self, model_class, *expressions):
        self.model_class = model_class
        self.expressions = expressions

    def statement(self):
        return select(self.model_class).where(*self.expressions)

    def one_or_none(self):
        return db.session.execute(self.statement()).scalar_one_or_none()

    def all(self):
        return db.session.execute(self.statement()).scalars().all()

    def first(self):
        return db.session.execute(self.statement()).scalars().first()

    def count(self):
        return len(self.all())


# TODO: Move this too, probably
def select_where(*expressions : BinaryExpression):
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo
    return SelectWrapper(model, *expressions)


# Helper function to upload profile picture.
# For user probably best to just use current_user
def image_upload(form : ImageUploadForm, user : User):
    filename = form.generate_filename()
    relative_path = f"uploads/{filename}" 

    # Translates to full path: app/static/uploads/{filename}
    full_path = os.path.join('app/static', relative_path) 
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    form.image.data.save(full_path)

    user.profile_picture = relative_path
    db.session.commit()