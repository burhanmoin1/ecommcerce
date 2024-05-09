from django.contrib.auth.backends import BaseBackend
from .models import SuperUser
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, login=None, password=None):
        superuser = None

        # Check if the input is an email or username
        if "@" in login:  # Likely an email
            try:
                superuser = SuperUser.objects.get(email=login)  # Fetch by email
            except SuperUser.DoesNotExist:
                return None
        else:  # Otherwise, assume it's a username
            try:
                superuser = SuperUser.objects.get(username=login)  # Fetch by username
            except SuperUser.DoesNotExist:
                return None

        # If superuser is found, check if the password matches
        if superuser and check_password(password, superuser.password):
            return superuser  # Successful authentication
        else:
            return None  # Authentication failed