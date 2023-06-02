import django
import os
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatApi.settings")

from channels.routing import ProtocolTypeRouter, URLRouter

from chat.channelsmiddleware import TokenAuthMiddleware
import chat.routing


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket':TokenAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})


django.setup()
