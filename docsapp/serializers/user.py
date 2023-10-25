from docsapp.models.user import Profile
from docsapp.serializers.authuser import AuthUserSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name')
    user = AuthUserSerializer(read_only = True)
    class Meta:
        model = Profile
        fields = ['user', 'id', 'tags']