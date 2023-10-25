from django.db import models
from django.utils.text import slugify
from docsapp.models.editable import Editable
from docsapp.models.user import Profile

class Comment(models.Model):
    parent_doc = models.ForeignKey(Editable, on_delete=models.CASCADE)
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=256)
    lineno = models.BigIntegerField()

    def __str__(self):
        return self.content

    @property
    def commenter_indexing(self):
        return self.commenter.user.username
    @property
    def parent_doc_indexing(self):
        return self.parent_doc.id