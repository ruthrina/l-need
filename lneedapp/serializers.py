from rest_framework import serializers
from django.contrib.auth.models import User
from .models import loginLogic, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user




class loginLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = loginLogic
        fields = ('first_login',)  # Include other fields if needed        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'bio', 'interests', 'location', 'age', 'profileImage')
