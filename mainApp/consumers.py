# # consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     print("NotificationConsumer")
#     async def connect(self):
#         print("connect")
#         self.group_name = f"user_{self.scope['url_route']['kwargs']['user_id']}"  # Use user_id from URL
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         print("disconnect")
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get('message', '')

#         # Echo back the received message
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     # Send notification to WebSocket
#     async def send_notification(self, event):
#         print("send_notification")
#         notification = event['notification']
#         await self.send(text_data=json.dumps({
#             'notification': notification
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        # print(self.scope['url_route']['kwargs']['user_id'])
        self.group_name = f"user_{self.scope['url_route']['kwargs']['user_id']}"

        # Add user to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect")
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle messages received from the WebSocket (optional)
        data = json.loads(text_data)
        print("Received message:", data)

    async def send_notification(self, event):
        # Handle the notification from the backend
        notification = event["notification"]
        await self.send(text_data=json.dumps({
            "notification": notification
        }))
