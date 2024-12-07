import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import accounts.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collaborative_code_editor.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/online_users/", OnlineUsersConsumer.as_asgi()),  # Update path to match your consumer route
path("ws/chat/", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})