import os
import chat.routing
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalproject.settings")

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AuthMiddlewareStack(
      URLRouter(
          chat.routing.websocket_urlpatterns
      )
  )
})

