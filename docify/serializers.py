import json
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .models import User, Tag
from .documents import EditableDocument, CommentDocument

class EditableDocumentSerializer(DocumentSerializer):
    class Meta:
        document = EditableDocument
        fields = (
            'title',
            'content',
            'id',
            'creation_time',
            'restricted',
            'owner',
            'read_tags',
            'write_tags',
            'comments',
            'slug',
        )

class CommentDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CommentDocument
        fields = (
            'content',
            'lineno',
        )
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'id', 'tags']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']