from django.db import models
from django.utils.text import slugify
from django.core.validators import validate_slug
import uuid
from docsapp.models.user import Profile
from docsapp.models.tag import Tag
import datetime



class Editable(models.Model):
    title = models.CharField(max_length=30, blank=False)
    content = models.BinaryField(editable=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # creation_time = models.DateTimeField(auto_now_add=True)
    restricted = models.BooleanField(default=False)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    read_tags = models.ManyToManyField(Tag, related_name="readable", blank=True)
    write_tags = models.ManyToManyField(Tag, related_name="writeable", blank=True)
    accessors = models.ManyToManyField(Profile, related_name="accessibles", blank=True)
    slug = models.SlugField(default='', null = False, validators=[validate_slug])

    @property
    def read_tags_indexing(self):
        return [read_tag.name for read_tag in self.read_tags.all()]
    @property
    def write_tags_indexing(self):
        return [write_tag.name for write_tag in self.write_tags.all()]
    @property
    def accessors_indexing(self):
        return [accessor.prof_username for accessor in self.accessors.all()]
    @property
    def owner_indexing(self):
        return self.creator.user.username
    @property
    def get_content(self):
        return self.content.decode('ascii')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Editable, self).save(*args, **kwargs)