from rest_framework import generics, permissions
from .models import Message, ChatRoom
from .serializers import MessageSerializer

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        chat_room = ChatRoom.objects.get(match_id=match_id)
        return Message.objects.filter(chat_room=chat_room)

    def perform_create(self, serializer):
        match_id = self.kwargs['match_id']
        chat_room = ChatRoom.objects.get(match_id=match_id)
        serializer.save(sender=self.request.user, chat_room=chat_room) 