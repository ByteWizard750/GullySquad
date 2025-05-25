from rest_framework import serializers
from .models import Message
from users.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'content', 'timestamp')
        read_only_fields = ('id', 'sender', 'timestamp') 