from django.contrib import admin

# Register your models here.
from .models import *
from .documents import *

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Editable)
admin.site.register(Comment)