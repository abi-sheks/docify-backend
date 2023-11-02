from django.db import models
from django.utils.text import slugify
from django.core.validators import validate_email, validate_slug
import uuid
from django.contrib.auth.models import User 


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField('docsapp.Tag', related_name="users")
    prof_username = models.SlugField(default='', null = False, validators=[validate_slug])

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        self.prof_username = self.user.username
        super(Profile, self).save(*args, **kwargs)