from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from docsapp.documents.editable import EditableDocument

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