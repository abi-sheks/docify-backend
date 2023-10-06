from django.contrib import admin

# Register your models here.
from docsapp.models.tag import Tag
from docsapp.models.editable import Editable
from docsapp.models.comment import Comment
from docsapp.models.user import Profile
from .documents import *

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Editable)
admin.site.register(Comment)