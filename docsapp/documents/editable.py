from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from docsapp.models.editable import Editable 
from docsapp.models.comment import Comment
from docsapp.models.tag import Tag
from docsapp.models.user import Profile

@registry.register_document
class EditableDocument(Document):
    owner = fields.TextField(attr='owner_indexing')
    read_tags = fields.TextField(attr='read_tags_indexing')
    write_tags = fields.TextField(attr='write_tags_indexing')
    comments = fields.NestedField(properties = {
        'content' : fields.TextField(),
        'lineno' : fields.IntegerField()
    })
    class Index:
        name="documents"
    
    class Django:
        model = Editable

        fields = [
            'title',
            'content',
            'creation_time',
            'restricted',
            'id',
            'slug',
        ]
        related_models = [Comment, Tag, Profile]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Comment):
            return related_instance.parent_doc
        elif isinstance(related_instance, Tag):
            if self.read_tags is not None and related_instance.name in self.read_tags:
                return related_instance.readable.all()
            elif self.write_tags is not None and related_instance.name in self.write_tags:
                return related_instance.writeable.all()
        elif isinstance(related_instance, Profile):
            return related_instance.editable_set.all()
