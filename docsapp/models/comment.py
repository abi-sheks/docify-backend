from django.db import models
import uuid
from django.utils.text import slugify
from docsapp.models.editable import Editable
from docsapp.models.user import Profile

class Comment(models.Model):
    parent_doc = models.ForeignKey(Editable, on_delete=models.CASCADE, related_name='comments', null=True)
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=256)
    comment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.content

    @property
    def commenter_indexing(self):
        return self.commenter.user.username
    @property
    def parent_doc_indexing(self):
        return self.parent_doc.id