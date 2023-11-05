from docsapp.models.comment import Comment
from docsapp.models.editable import Editable
from docsapp.models.user import Profile
from docsapp.serializers.comment import CommentSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from docsapp.permissions import CommentsAccessPermission

class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, 
                        #   CommentsAccessPermission
                          ]
    authentication_classes=[TokenAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # def get_queryset(self):
    #     docID = self.request.data.get('parent_doc')
    #     try:
    #         return Comment.objects.filter(parent_doc__id=docID)
    #     except Comment.DoesNotExist:
    #         return None