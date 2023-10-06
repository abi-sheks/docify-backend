from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from docsapp.documents.comment import CommentDocument

class CommentDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CommentDocument
        fields = (
            'content',
            'lineno',
        )