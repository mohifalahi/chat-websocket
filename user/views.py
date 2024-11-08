import logging
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

from .serializers import BroadCastMessageSerializer

logger = logging.getLogger(__name__)


def index(request):
    """Renders the html template to watch the incoming messages to the client"""
    return render(request, "index.html")


class BroadCastAPIView(GenericAPIView):
    """
    Broadcasts messages to the websocket group
    and get the message from the serializer and validate it
    and calls the group_send method as a consumer
    and gets the receiver_count from the cache
    and returns the broadcast successful message and the number of receiver_count.
    """
    serializer_class = BroadCastMessageSerializer

    def post(self, request, *args, **kwargs):
        receiver_count = 0

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message = serializer.validated_data["message"]
            logger.info(f"Message to broadcast: {message}")

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "test", {"type": "chat_message", "message": message}
        )
        logger.info("Broadcast sent to group.")

        time.sleep(1)
        receiver_count = cache.get("receiver_count", 0)
        cache.clear()

        return Response(
            {
                "message": "message broadcast successfully",
                "receiver_count": receiver_count,
            }
        )
