from django.urls import re_path
from .consumers import OnlineUsersConsumer

websocket_urlpatterns = [
    re_path(r'ws/online_users/$', OnlineUsersConsumer.as_asgi()),  # WebSocket URL
]
