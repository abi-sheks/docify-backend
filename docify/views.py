from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from .documents import EditableDocument, CommentDocument
from .models import User, Tag
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, mixins, permissions
from docify.permissions import IsCreatorPermission
from django.http import Http404
from .serializers import EditableDocumentSerializer, UserSerializer, TagSerializer
# Create your views here.

class EditableDocumentView(BaseDocumentViewSet):
    permissions = [IsAuthenticated]
    document = EditableDocument
    serializer_class = EditableDocumentSerializer
    lookup_field = 'slug'
    search_fields = {
        'id',
        'slug',
    }

class UserList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    permissions = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
class UserByTag(generics.ListCreateAPIView):
    permissions = [IsAuthenticated]
    def get_queryset(self):
        tag = self.kwargs['tag']
        try:
            return User.objects.filter(read_tags__name=tag, write_tags__name=tag)
        except User.DoesNotExist:
            raise Http404
    
class UserDetail(APIView):
    permissions = [IsAuthenticated]
    def get_user(self, slug):
        try:
            return User.objects.get(slug=slug)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, slug, format=None):
        user = self.get_user(slug)
        srl = UserSerializer(user)
        return Response(srl.data)
    
    def put(self, request, slug, format=None):
        user = self.get_user(slug)
        srl = UserSerializer(user)
        if srl.is_valid():
            srl.save()
            return Response(srl.data)
        return Response(srl.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, format=None):
        user = self.get_user(slug)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TagList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    permissions = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
class TagsByMember(generics.ListCreateAPIView):
    permissions = [IsAuthenticated]
    serializer_class = TagSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            return Tag.objects.filter(users__email=user.email)
        except Tag.DoesNotExist:
            return None
class TagDetail(APIView):
    permissions = [IsAuthenticated]
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


    

