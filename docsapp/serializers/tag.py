from docsapp.models.tag import Tag
from rest_framework import serializers
from docsapp.models.user import Profile
from docsapp.serializers.user import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='prof_username', queryset=Profile.objects.all())
    users = serializers.SlugRelatedField(many = True, slug_field = 'prof_username', queryset=Profile.objects.all())
    admins = serializers.SlugRelatedField(many = True, slug_field='prof_username', queryset=Profile.objects.all())
    class Meta:
        model = Tag
        fields = ['name', 'users', 'creator', 'slug', 'id', 'admins']