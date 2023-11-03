from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from docsapp.models.tag import Tag
from docsapp.serializers.tag import TagSerializer
from docsapp.permissions import TagEditPermission


class TagList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # def get_queryset(self):
    #     user = self.request.user
    #     try:
    #         return Tag.objects.filter(users__user=user)
    #     except Tag.DoesNotExist:
    #         return None
    
class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TagEditPermission]
    authentication_classes=[TokenAuthentication]
    lookup_field = 'id'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

