from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, ValidationError
from werkzeug.utils import secure_filename
from flask_login import current_user
from PIL import Image
import io
from flask import current_app



# TODO: probably need to check for file size too i assume... profile pictures should be 10kx10k resolution or smth

class ImageUploadForm(FlaskForm):
    image = FileField('Choose picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only .jpg, .jpeg or .png files are allowed.')
    ])
    submit = SubmitField('Upload Image')

def validate_image(form, field):
    if field.data:
        allowed_mime_types = {'image/jpeg', 'image/png'}
        if field.data.mimetype not in allowed_mime_types:
            raise ValidationError('Invalid file type (MIME). Only JPEG and PNG images are allowed.')

        # Check file size (max 2MB)
        field.data.stream.seek(0, io.SEEK_END)
        file_size = field.data.stream.tell()
        field.data.stream.seek(0)
        max_size = 2 * 1024 * 1024
        if file_size > max_size:
            raise ValidationError('File size must be less than 2MB.')

        try:
            image = Image.open(field.data)
            width, height = image.size

            if width < 128 or height < 128:
                raise ValidationError('Image is too small. Minimum size is 128x128 pixels.')

            # Crop to square
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            image = image.crop((left, top, right, bottom))

            # Resize to 512x512
            image = image.resize((512, 512))

            # Save to memory buffer
            buffer = io.BytesIO()
            format = 'JPEG' if field.data.mimetype == 'image/jpeg' else 'PNG'
            image.save(buffer, format=format)
            buffer.seek(0)

            # ✅ Attach to form
            form._processed_image = buffer

        except Exception as e:
            raise ValidationError('Image processing failed. Please upload a valid image.')

