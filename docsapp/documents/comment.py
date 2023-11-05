from django_elasticsearch_dsl import fields, Document
from docsapp.models.comment import Comment
from django_elasticsearch_dsl.registries import registry

@registry.register_document
class CommentDocument(Document):
    parent_doc = fields.TextField(attr='parent_doc_indexing')
    commenter = fields.TextField(attr='commenter_indexing')
    class Index:
        name = "comments"
    
    class Django:
        model = Comment

        fields = [
            'content',
            'comment_id',
        ]