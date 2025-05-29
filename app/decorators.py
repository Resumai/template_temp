
from functools import wraps
from flask import session, abort
from app.config import BLOCKED_FEATURES

def role_required(*roles, block_key=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role')

            # Role check
            if user_role not in roles:
                return abort(403)

            # Block check
            if block_key and BLOCKED_FEATURES.get(block_key, False):
                if user_role != 'admin':
                    return abort(503, description="Temporarily unavailable")

            return f(*args, **kwargs)
        return decorated_function
    return decorator
