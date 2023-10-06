from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, mixins
from docsapp.models.tag import Tag
from docsapp.serializers.tag import TagSerializer


class TagList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    permissions = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
class TagsByMember(generics.ListCreateAPIView):
    # permissions = [IsAuthenticated]
    serializer_class = TagSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            return Tag.objects.filter(users__user=user)
        except Tag.DoesNotExist:
            return None
class TagDetail(APIView):
    # permissions = [IsAuthenticated]
    def get_tag_by_name(self, slug):
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            return None
    def get(self, request, format=None):
        tag_name = self.request.query_params.get('name')
        if tag_name is not None:
            tag = self.get_tag_by_name(tag_name)
            srl = TagSerializer(tag)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(srl.data)
    
    def put(self, request, name, format=None):
        tag = self.get_tag_by_name(name)
        if tag.creator.email != request.user.email:
            raise Http404
        else:
            srl = TagSerializer(tag, data=request.data)
            if srl.is_valid():
                srl.save()
                return Response(srl.data)
            return Response(srl.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, name, format=None):
        tag = self.get_tag_by_name(name)
        if tag.creator.email == request.user.email:
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404
