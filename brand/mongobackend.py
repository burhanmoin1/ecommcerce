from django.contrib.auth.backends import BaseBackend
from .models import *
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            brand = BrandAccount.objects.get(email=email)
            if check_password(password, brand.password):
                return brand
        except BrandAccount.DoesNotExist:
            return None

    def get_brand(self, brand_id):
        try:
            return BrandAccount.objects.get(pk=brand_id)
        except BrandAccount.DoesNotExist:
            return None