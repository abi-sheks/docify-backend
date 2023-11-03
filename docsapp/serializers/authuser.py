from django.contrib.auth.models import User
from rest_framework import serializers

class AuthUserSerializer(serializers.ModelSerializer):
    username= serializers.CharField(min_length=8)
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
