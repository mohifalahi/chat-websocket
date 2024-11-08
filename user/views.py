from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

from .serializers import BroadCastMessageSerializer

from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
import time

import logging
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


class BroadCastAPIView(GenericAPIView):
    serializer_class = BroadCastMessageSerializer

    def post(self, request, *args, **kwargs):
        receiver_count = 0 # count of websocket connection that message sent
        # TODO : get message from body and send to all websocket connection and return receiver count

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message = serializer.validated_data["message"]
            logger.info(f"Message to broadcast: {message}")

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "test",
            {
                "type": "chat_message",
                "message": message
            }
        )
        logger.info("Broadcast sent to group.")

        time.sleep(1)
        receiver_count = cache.get("receiver_count", 0)
        cache.clear()

        return Response({"message": "message broadcast successfully", "receiver_count": receiver_count})
