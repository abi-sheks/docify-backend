from django.urls import path, include
from .views.editable import EditableDocumentView
from .views.user import UserList, UserDetail
from .views.tag import TagDetail, TagList, TagsByMember
from rest_framework.urlpatterns import format_suffix_patterns

doc_list = EditableDocumentView.as_view({
    'get' : 'list',
})
doc_detail = EditableDocumentView.as_view({
    'get' : 'retrieve',
})


urlpatterns = [
    path('docs/', doc_list, name='doc_list'),
    path('docs/<slug:slug>', doc_detail, name='doc_detail'),
    path('users/', UserList.as_view(), name='users'),
    path('users/<slug:slug>', UserDetail.as_view(), name='user'),
    path('tags/', TagList.as_view(), name='tags'),
    path('tags/tag/', TagDetail.as_view(), name='tag'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

