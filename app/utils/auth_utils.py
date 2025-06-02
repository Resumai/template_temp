from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles, block_key=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)  # Unauthorized

            # Role check
            if current_user.role not in roles:
                abort(403)  # Forbidden

            # Optional feature-block check
            if block_key and not current_user.has_feature(block_key):
                abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorator
