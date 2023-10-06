from django.db import models
from django.utils.text import slugify
from django.core.validators import validate_slug
import uuid
from docsapp.models.user import Profile
from docsapp.models.tag import Tag



class Editable(models.Model):
    title = models.CharField(max_length=30, blank=False)
    content = models.CharField(max_length=2000, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_time = models.TimeField()
    restricted = models.BooleanField(default=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    read_tags = models.ManyToManyField(Tag, related_name="readable")
    write_tags = models.ManyToManyField(Tag, related_name="writeable")
    slug = models.SlugField(default='', null = False, validators=[validate_slug])

    @property
    def read_tags_indexing(self):
        return [read_tag.name for read_tag in self.read_tags.all()]
    @property
    def write_tags_indexing(self):
        return [write_tag.name for write_tag in self.write_tags.all()]
    @property
    def owner_indexing(self):
        return self.owner.user.username

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Editable, self).save(*args,)