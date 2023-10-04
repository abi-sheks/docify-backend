from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/docs/(?P<id>\w+)/$', consumers.EditableConsumer.as_asgi()),
]