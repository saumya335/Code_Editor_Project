import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the room group
        self.room_group_name = "online_users_group"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data.get('status')

        # Logic to handle online/offline users status
        if status:
            users = await self.get_users_by_status(status)
            await self.send(text_data=json.dumps({
                'status': status,
                'users': users
            }))

    async def get_users_by_status(self, status):
        # Placeholder logic to return simulated online/offline users
        if status == "online":
            return ["User1", "User2"]  # Modify this with actual database query logic
        elif status == "offline":
            return ["User3", "User4"]  # Modify this with actual database query logic
        return []


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Process the message and generate a response (can integrate AI or predefined responses)
        response = await self.generate_response(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': response
        }))

    async def generate_response(self, message):
        # For now, return a simple predefined response or integrate an API for chatbot functionality
        return f"Chatbot: You said '{message}'"