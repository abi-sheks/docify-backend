from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from docsapp.documents.comment import CommentDocument
from docsapp.models.user import Profile
from docsapp.models.editable import Editable
from docsapp.models.comment import Comment
from docsapp.utils import isAccessible, isReader

class CommentDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CommentDocument
        fields = (
            'content',
            'parent_doc',
            'commenter',
            'comment_id',
        )

class CommentSerializer(serializers.ModelSerializer):
    commenter = serializers.SlugRelatedField(slug_field='prof_username', queryset=Profile.objects.all())
    parent_doc = serializers.PrimaryKeyRelatedField(queryset=Editable.objects.all())
    class Meta:
        model = Comment
        fields = ['content', 'comment_id' , 'commenter', 'parent_doc' ]