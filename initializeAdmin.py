import os
import sys

# import data as data
import django
from django.contrib.auth.hashers import make_password

# Add the root directory of your Django project to the import search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuthorizationUnit.settings')

# Initialize Django
django.setup()

from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import jwt
import requests
from django.db import IntegrityError


try:
    # Create a user (example only)
    user, created = User.objects.get_or_create(username='admin', is_superuser=True)
    if created:
        user.set_password('admin')  # Set the password for a newly created user # PBKDF2
        user.save()
except IntegrityError:
    print('Username already exists. Please register with a different username.')
    # Handle the prompt to register with a different username
    # You can ask the user to input a new username and try creating the user again
    exit()  # Exit the script if the username already exists


# Generate a JWT token for the user
payload = {
    'user_id': user.id,
    'username': user.username,
    'is_superuser': user.is_superuser
}
token = jwt.encode(payload, SECRET_KEY)

# Set the Authorization header with the JWT token
headers = {
    'Authorization': f'Bearer {token}'
}

# # Make a request to the Django admin interface
# response = requests.get('http://localhost:8000/admin/', headers=headers)
#
# # Check the response
# if response.status_code == 200:
#     print('Successfully accessed the admin interface.')
# else:
#     print('Failed to access the admin interface.')