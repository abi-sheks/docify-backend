from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, FilteringFilterBackend, OrderingFilterBackend
from rest_framework.permissions import IsAuthenticated
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_QUERY_CONTAINS,
)
from docsapp.serializers.editable import EditableDocumentSerializer, EditableSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from docsapp.models.user import Profile
from docsapp.models.editable import Editable
from docsapp.documents.editable import EditableDocument
from docsapp.serializers.editable import EditableDocumentSerializer
from docsapp.permissions import IsCreatorPermission




class EditableDocumentView(BaseDocumentViewSet):
    # permissions = [IsAuthenticated]
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
    serializer_class = EditableSerializer
    queryset = Editable.objects.all()

class EditableUpdationView(RetrieveUpdateDestroyAPIView):
    # permissions = [IsCreatorPermission]
    lookup_field = 'id'
    queryset = Editable.objects.all()
    serializer_class = EditableSerializer
