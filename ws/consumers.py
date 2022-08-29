import json
from time import sleep
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer
from photobatle.serializers import *


class WSTest(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user'] if self.scope['user'] != 'AnonymousUser' else None
        if user:
            self.personal_room = str(user)
            self.general_room = 'general_room'

            await self.channel_layer.group_add(
                self.personal_room,
                self.channel_name
            )

            await self.channel_layer.group_add(
                self.general_room,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.personal_room,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            self.general_room,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        await self.channel_layer.group_send(
            self.personal_room,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        await self.channel_layer.group_send(
            self.general_room,
            {
                'type': 'chat_message',
                'message': 'message'
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

