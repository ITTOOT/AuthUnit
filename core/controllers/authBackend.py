# backend.py
import jwt
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from AuthorizationUnit import settings
from django.contrib.auth.hashers import check_password
from jwt.exceptions import DecodeError

# Authentication Controller
class JWTAuthenticationBackend(BaseBackend):
    """ The user passed to the backend from the view document is authenticated here, with JWT """
    # Authenticate
    def authenticate(self, request, username=None, password=None, token=None, **kwargs):
        User = get_user_model()
        try:
            if token is not None:
                # Get the validated user including the token
                payload = jwt.decode(token.encode('utf-8'), settings.JWT_AUTH['JWT_SECRET_KEY'])
                # Get the ID from teh payload
                user_id = payload['user_id']
                # Check if the user exists and is verified
                user = User.objects.get(id=user_id, username=username, is_verified=True)

                # Verify the password and return the authenticated user
                if check_password(password, user.password):
                    return user
            else:
                # Handle the case when the token is not provided or invalid
                pass
        except DecodeError:
            # Handle the case where the token is invalid
            return None
        except (User.DoesNotExist, jwt.ExpiredSignatureError):
            pass
        return None

    # Get User
    def get_user(self, user_id):
        User = get_user_model()
        try:
            # Return the user with the ID
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

