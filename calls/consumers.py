import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_message',
                'message': {
                    'type': 'peer-joined',
                    'sender': self.channel_name,
                },
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_message',
                'message': {
                    'type': 'peer-left',
                    'sender': self.channel_name,
                },
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        data['sender'] = self.channel_name
        target = data.get('target')

        if target:
            # Direct message to one specific peer (offer/answer/ICE candidate)
            await self.channel_layer.send(
                target,
                {
                    'type': 'signal_message',
                    'message': data,
                }
            )
        else:
            # No target — broadcast to the whole room (used for peer-joined/peer-left)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'signal_message',
                    'message': data,
                }
            )

    async def signal_message(self, event):
        message = event['message']

        if message.get('sender') == self.channel_name:
            return

        await self.send(text_data=json.dumps(message))