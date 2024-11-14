from django.urls import path

from user import consumers

ws_urlpatterns = [
    path("ws/subscribe", consumers.ChatConsumer.as_asgi()),
]
