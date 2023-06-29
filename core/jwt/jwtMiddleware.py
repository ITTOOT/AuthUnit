from django.contrib.auth.models import User
from django.dispatch import Signal
from django.contrib.auth import get_user_model
from django.utils import timezone
from jwt import InvalidTokenError
from core.models.userModels import UserLoginLog
import jwt
from AuthorizationUnit.settings import SECRET_KEY

# Create a signal for breach alerts
breach_alert = Signal()

# JWT Authorization Middleware
class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # JWT authentication logic here
        # Get the header from the request
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        if authorization_header:
            try:
                # Retrieve the JWT token from the header
                _, token = authorization_header.split(' ')
            except ValueError:
                # Handle cases where the header doesn't have the expected format
                # Log an error or raise an exception, depending on your requirements
                pass
        else:
            # Handle cases where the header is not present
            # Log an error or raise an exception, depending on your requirements
            pass

        # Verify and decode the token
        user = None
        try:
            # Ensure that you verify the token's authenticity, expiration,
            # and any other relevant checks. If the token is valid, you can
            # set the user variable to the appropriate user object based on
            # the decoded token. If the token is invalid or the user does not exist,
            # user remains None.

            if hasattr(request, 'user') and request.user.is_authenticated:
                username = request.META.get('REMOTE_USER', '')

                # Decode token
                decoded_token = decode_jwt_token(token)

                # If the token is valid, set the user object
                user = get_user_model().objects.get(id=decoded_token['user_id'])

                # If the user is authenticated, log the login attempt
                ip_address = request.META.get('REMOTE_ADDR', '')
                UserLoginLog.objects.create(user=user, ip_address=ip_address, login_time=timezone.now())

                # Emit the breach_alert signal with the user and IP address as keyword arguments
                breach_alert.send(sender=self.__class__, user=user, ip_address=ip_address)

            response = self.get_response(request)
            return response
        except (InvalidTokenError, get_user_model().DoesNotExist):
            # If the token is invalid or the user does not exist, do not set the user object
            pass

        # If the user is authenticated, log the login attempt
        if user:
            ip_address = request.META.get('REMOTE_ADDR', '')
            UserLoginLog.objects.create(user=user, ip_address=ip_address, login_time=timezone.now())

        # Continue with the request processing
        request.user = user
        response = self.get_response(request)
        return response


def decode_jwt_token(token):
    # Replace the 'YOUR_SECRET_KEY' with your actual secret key used for JWT signing
    secret_key = SECRET_KEY
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.InvalidTokenError:
        # Handle invalid token, such as logging an error or raising an exception
        return None


def getCurrentUser(request):
    # Access the authenticated user
    user = request.user

    # Access the JWT token
    authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
    if authorization_header:
        _, token = authorization_header.split(' ')
        decoded_token = decode_jwt_token(token)
        # You can use the decoded token for further processing

    # Further function logic here

    return user  # Return the user object