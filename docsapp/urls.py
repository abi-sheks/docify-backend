from django.urls import path
from docsapp.views.editable import EditableDocumentView, EditableCreationView, EditableUpdationView
from docsapp.views.user import UserList, UserDetail
from docsapp.views.tag import TagDetail, TagList
from docsapp.views.auth import RegisterView, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from . import consumers


urlpatterns = [

    path('docs/', EditableCreationView.as_view(), name='docs'),
    path('docs/search', EditableDocumentView.as_view({'get' : 'list'}), name='docs'),
    path('docs/create/', csrf_exempt(EditableCreationView.as_view()), name = 'doc_create'),
    path('docs/<slug:id>', csrf_exempt(EditableUpdationView.as_view()), name='doc_detail'),

    path('users/', UserList.as_view(), name='users'),
    path('users/<slug:slug>', UserDetail.as_view(), name='user'),

    path('tags/', csrf_exempt(TagList.as_view()), name='tags'),
    path('tags/<slug:id>', csrf_exempt(TagDetail.as_view())),
    
    path('auth/login/', csrf_exempt(LoginView.as_view()), name='login'),
    path('auth/register/', csrf_exempt(RegisterView.as_view()), name='register'),
    path('logout/', csrf_exempt(LogoutView.as_view()), name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

websocket_urlpatterns = [
    path('ws/docs/<slug:id>', consumers.EditableConsumer.as_asgi()),
]
