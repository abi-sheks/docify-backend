from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from docsapp.models.tag import Tag
from docsapp.serializers.tag import TagSerializer
from docsapp.authentication import CsrfExemptSessionAuthentication

from docsapp.permissions import TagEditPermission


class TagList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[CsrfExemptSessionAuthentication]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TagEditPermission]
    authentication_classes=[CsrfExemptSessionAuthentication]
    lookup_field = 'id'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

