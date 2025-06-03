from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, ValidationError
from werkzeug.utils import secure_filename
from flask_login import current_user



# TODO: probably need to check for file size too i assume... profile pictures should be 10kx10k resolution or smth
class ImageUploadForm(FlaskForm):
    image = FileField('Choose picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only .jpg, .jpeg or .png files are allowed.')
    ])
    submit = SubmitField('Upload Image')

    # Because file endings can be changed, we check the MIME type too 
    # wtforms runs automatically every method defined with 'def validate_...(...):'
    # This happens when form.validate_on_submit() is called if from Flask-WTF
    # If using WTForms, its forms.validate() is called automatically
    def validate_image(form, field):
        if field.data:
            allowed_mime_types = {'image/jpeg', 'image/png'}
            if field.data.mimetype not in allowed_mime_types:
                raise ValidationError('Invalid file type (MIME). Only JPEG and PNG images are allowed.')
                

    # Returns a secure filename based on MIME type and current user ID.
    def generate_filename(self) -> str:
        image = self.image.data
        mime_to_ext = {
            'image/jpeg': 'jpg',
            'image/png': 'png'
        }
        ext = mime_to_ext.get(image.mimetype)
        if not ext:
            raise ValueError("Unsupported MIME type for filename generation.")
        return secure_filename(f"uid_{current_user.id}_pic.{ext}")
