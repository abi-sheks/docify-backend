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
from docsapp.utils import isCreator, isAccessible




class EditableDocumentView(BaseDocumentViewSet):
    #dont need to filter by restriction or user here for queryset, as filtering happens on frontend.
    # but security risk? so this view is still unsafe.
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
        # can just fetch read tags, as by mechanism, write tags are also read tags
        user_docs = list(Editable.objects.filter(read_tags__users__user=user).distinct())
        user_accessible_docs = list(Editable.objects.filter(accessors__prof_username=user.username).distinct())
        user_available_docs = []
        for doc in user_docs:
            if(isAccessible(user.username , doc)):
                user_available_docs.append(doc)
        final_docs = []
        final_docs.extend(user_available_docs)
        #performs a union of lists basically
        for doc in user_accessible_docs:
            if doc not in user_available_docs:
                final_docs.append(doc)
                
        return final_docs

    
class EditableUpdationView(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated, DocMutatePermission]
    authentication_classes=[TokenAuthentication]
    lookup_field = 'id'
    queryset = Editable.objects.all()
    serializer_class = EditableSerializer
