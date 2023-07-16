import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
# from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
from django.contrib.auth import get_user_model
User = get_user_model()
from chat.models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        user = self.scope['user']
        chat_room = f"user_chatroom_{user.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })


    async def websocket_receive(self, event):
        print("received", event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
       
        if not msg:
            print("ERROR::: empty message")
            return False
        
        sent_by_user = await self.get_user_objects(sent_by_id)
        send_to_user = await self.get_user_objects(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        # print("ddddddddddddddddddd",send_to_user, thread_obj)
        
        if not send_to_user and sent_by_user:
            print("Error: user id is incorrrect")

        if not thread_obj:
            print("Error: Thread id is incorrect or Not Exists")

        await self.create_chat_message(thread_obj, sent_by_user, msg)

        other_user_chat_room = f"user_chatroom_{send_to_id}"
        self_user = self.scope['user']

        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id,
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        # await self.send({
        #     'type': 'websocket.send',
        #     'text': json.dumps(response)
        # })



    async def websocket_disconnect(self, event):
        print("disconnected", event)


    @database_sync_to_async
    def get_user_objects(self, user_id):
        qs = User.objects.filter(id= user_id)
        if qs.exists():
            obj = qs.first()

        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()

        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        ChatMessage.objects.create(thread=thread, user=user, message=msg)
       

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })






















# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
