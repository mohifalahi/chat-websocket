import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "test"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        logger.info(f"Message from WebSocket client: {message}")


    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": message
        }))
        logger.info(f"Broadcasted message received: {message}")

        receiver_count = cache.get("receiver_count", 0) + 1
        cache.set("receiver_count", receiver_count)

        await self.close() #To close the connection followed by the first message broadcasted


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

