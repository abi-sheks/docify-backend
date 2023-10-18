from django.db import models
from django.utils.text import slugify
import uuid
from django.core.validators import validate_slug


class Tag(models.Model):
    name = models.CharField(max_length=10, blank=False, primary_key=True)
    creator = models.ForeignKey('docsapp.Profile', related_name='creator', null=True, on_delete=models.CASCADE)
    slug = models.SlugField(default='', null = False, validators=[validate_slug])

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)