from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from docsapp.models.tag import Tag
from docsapp.serializers.tag import TagSerializer
from docsapp.permissions import TagEditPermission


class TagList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TagEditPermission]
    lookup_field = 'id'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

