from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework.permissions import IsAuthenticated
from docsapp.documents.editable import EditableDocument
from docsapp.serializers.editable import EditableDocumentSerializer



class EditableDocumentView(BaseDocumentViewSet):
    permissions = [IsAuthenticated]
    document = EditableDocument
    serializer_class = EditableDocumentSerializer
    lookup_field = 'slug'
    search_fields = {
        'id',
        'slug',
    }