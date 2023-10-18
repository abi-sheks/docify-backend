from docsapp.models.tag import Tag
from rest_framework import serializers
from docsapp.models.user import Profile
from docsapp.serializers.user import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only = True)
    users = serializers.SlugRelatedField(many = True, slug_field = 'slug', queryset=Profile.objects.all())
    class Meta:
        model = Tag
        fields = ['name', 'users', 'creator', 'slug']