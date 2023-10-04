import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class EditableConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["id"]
        self.room_group_name = f"doc_{self.room_name}"
        print(self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name,
        )
        print(self.room_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard (
            self.room_group_name, self.channel_name
        )

    async def receive(self, bytes_data):
        print(bytes_data)
        print(type(bytes_data))

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type" : "doc.content", "content" : bytes_data}
        # )

    # def doc_content(self, event):
    #     bytes_data = event['content']
    #     self.send(bytes_data=bytes_data)