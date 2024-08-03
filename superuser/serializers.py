from rest_framework_mongoengine import serializers
from django.contrib.auth.hashers import make_password
from .models import SuperUser

class SuperUserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = SuperUser
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
