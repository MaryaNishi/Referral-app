from rest_framework import serializers
from .models import User

class UserPhoneNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']