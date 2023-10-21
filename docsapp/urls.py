from django.urls import path, re_path, include
from docsapp.views.editable import EditableDocumentView, EditableCreationView, EditableUpdationView
from docsapp.views.auth import OAuthLogin
from docsapp.views.user import UserList, UserDetail
from docsapp.views.tag import TagDetail, TagList, TagsByMember, IndividualTagReadOnly
from docsapp.views.auth import OAuthLogin, OAuthRedirect, LogoutView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from . import yconsumer

tag_detail_read = IndividualTagReadOnly.as_view({
    'get' : 'retrieve',
})


urlpatterns = [
    path('docs/', EditableCreationView.as_view(), name='docs'),
    path('docs/search', EditableDocumentView.as_view({'get' : 'list'}), name='docs'),
    path('docs/create/', csrf_exempt(EditableCreationView.as_view()), name = 'doc_create'),
    path('docs/<slug:id>', csrf_exempt(EditableUpdationView.as_view()), name='doc_detail'),
    path('users/', UserList.as_view(), name='users'),
    path('users/<slug:slug>', UserDetail.as_view(), name='user'),
    path('tags/', csrf_exempt(TagList.as_view()), name='tags'),
    path('tags/<slug:id>', csrf_exempt(TagDetail.as_view())),
    path('auth/', OAuthLogin.as_view(), name='auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('oauth/', OAuthRedirect.as_view(), name='oauth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

websocket_urlpatterns = [
    path('ws/docs/<slug:id>', yconsumer.EditableConsumer.as_asgi()),
]
