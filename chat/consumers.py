from datetime import datetime
import json
from io import BytesIO

import PIL.Image as Image
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.images import ImageFile

from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        print(user_id)
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print("[ CONSUMER.RECEIVE ] TEST")
            image_temp = Image.open(BytesIO(bytes_data))

            room_id = self.room_name
            user = self.scope["user"]
            name = user.name
            tag = user.tag
            image = ImageFile(BytesIO(bytes_data), name=self.scope['user'].tag +
                                                        datetime.now().strftime("%Y_%m_%d_%H_%M_%S.") +
                                                        image_temp.format)
            new_msg = Message(user=user, room_id=room_id, image=image)
            new_msg.save()
            print(new_msg.image.path)
            print(f"[ receive image ] {name} ({tag})")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': new_msg.text,
                    'image': new_msg.image.url,
                    'user': name + " (" + tag + ")",
                    'avatar': user.avatar.url,
                    'date': new_msg.date.strftime("%d-%m-%Y %H:%M:%S")
                }
            )
            
        else:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            room_id = text_data_json['room_id']
            user = self.scope["user"]
            name = user.name
            tag = user.tag
            # date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            new_msg = Message(user=user, room_id=room_id, text=message)
            new_msg.save()
            print(f"[ receive ] {name} ({tag})")
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': new_msg.text,
                    'image': None,
                    'user': name + " (" + tag + ")",
                    'avatar': user.avatar.url,
                    'date': new_msg.date.strftime("%d-%m-%Y %H:%M:%S")
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        image = event['image']
        user = event['user']
        avatar = event['avatar']
        date = event['date']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'image': image,
            'user': user,
            'avatar': avatar,
            'date': date
        }))
