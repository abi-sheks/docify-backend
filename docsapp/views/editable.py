from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, FilteringFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_QUERY_CONTAINS,
)
from docsapp.serializers.editable import EditableDocumentSerializer, EditableSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from docsapp.models.editable import Editable
from docsapp.documents.editable import EditableDocument
from docsapp.serializers.editable import EditableDocumentSerializer
from docsapp.permissions import DocMutatePermission




class EditableDocumentView(BaseDocumentViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    document = EditableDocument
    serializer_class = EditableDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend,
        FilteringFilterBackend,
    ]
    search_fields = {
        'title',
        'id',
        'slug',
    }
    filter_fields = {
        'title' : {
        'field' : 'title',
        'lookups' : [
            LOOKUP_FILTER_PREFIX,
            LOOKUP_QUERY_CONTAINS,
        ]
        },
        'slug' : 'slug.raw',
    }
class EditableCreationView(ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    serializer_class = EditableSerializer
    def get_queryset(self):
        user = self.request.user
        # #can just fetch read tags, as by mechanism, write tags are also read tags
        user_docs = Editable.objects.filter(read_tags__users__user=user).distinct()
        return user_docs

    
class EditableUpdationView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated, DocMutatePermission]
    authentication_classes=[TokenAuthentication]
    lookup_field = 'id'
    queryset = Editable.objects.all()
    serializer_class = EditableSerializer
