from docsapp.models.comment import Comment
from docsapp.models.editable import Editable
from docsapp.models.user import Profile
from docsapp.serializers.comment import CommentSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from docsapp.permissions import CommentsAccessPermission
from docsapp.authentication import CsrfExemptSessionAuthentication


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, 
                          CommentsAccessPermission
                          ]
    authentication_classes=[CsrfExemptSessionAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer