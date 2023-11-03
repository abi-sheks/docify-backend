from django.contrib import admin

# Register your models here.
from docsapp.models.tag import Tag
from docsapp.models.editable import Editable
from docsapp.models.comment import Comment
from docsapp.models.user import Profile
from .documents import *

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'users', 'creator', 'slug']

class EditableAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'creator']
    readonly_fields = ['id',]



admin.site.register(Profile)
admin.site.register(Tag, TagAdmin)
admin.site.register(Editable, EditableAdmin)
admin.site.register(Comment)