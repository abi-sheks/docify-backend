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
    parent_doc = serializers.SlugRelatedField(slug_field='id', queryset=Profile.objects.all())
    class Meta:
        model = Comment
        fields = ['content', 'comment_id' , 'commenter', 'parent_doc' ]
    
    # def create(self, **validated_data):
    #     docID : str = self.context['request'].data.get('parent_doc')
    #     print(docID)
    #     commenter : str = self.context['request'].user.username
    #     print(f"Try is failing")
    #     try:
    #         doc = Editable.objects.filter(íd=docID)
    #         print(f"This is the doc")
    #         if(isReader(commenter, doc) and isAccessible(commenter, doc)):
    #             super(CommentSerializer, self).create(**validated_data)
    #         else:
    #             raise PermissionDenied("Not authorized to comment")
    #     except:
    #         return;
