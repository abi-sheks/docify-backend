from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from docsapp.models.user import Profile
from docsapp.serializers.user import UserSerializer
from django.http import Http404

class UserList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    permissions = [IsAuthenticated]
    queryset = Profile.objects.all()
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
            return Profile.objects.filter(read_tags__name=tag, write_tags__name=tag)
        except Profile.DoesNotExist:
            raise Http404
    
class UserDetail(APIView):
    permissions = [IsAuthenticated]
    def get_user(self, slug):
        try:
            return Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
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
    