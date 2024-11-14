import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """Handles websocket connections for live updates."""

    async def connect(self):
        """
        Called when a websocket connection is established
        and creates the room group name.
        """
        self.room_group_name = "test"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        """
        Called when a message is received from a client
        and parses the incoming json message and logs it.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        logger.info(f"Message from WebSocket client: {message}")

    async def chat_message(self, event):
        """
        Handles a broadcasted message from the group
        and sends the broadcasted message to the clients
        and logs the message, updates the receiver count in cache
        and closes the connection after the first broadcasted message received.
        """
        message = event["message"]
        await self.send(text_data=json.dumps({"type": "chat", "message": message}))
        logger.info(f"Broadcasted message received: {message}")

        receiver_count = cache.get("receiver_count", 0) + 1
        cache.set("receiver_count", receiver_count)

        await self.close()

    async def disconnect(self, close_code):
        """Called when a websocket connection is closed."""

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
