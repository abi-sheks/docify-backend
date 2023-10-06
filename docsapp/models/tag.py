from django.db import models
from django.utils.text import slugify
from django.core.validators import validate_slug


class Tag(models.Model):
    name = models.CharField(max_length=10, blank=False, primary_key=True)
    slug = models.SlugField(default='', null = False, validators=[validate_slug])

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)