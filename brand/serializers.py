from django_mongoengine import forms
from .models import *

class BrandAccountForm(forms.DocumentForm):
    class Meta:
        document = BrandAccount
        fields = '__all__' 