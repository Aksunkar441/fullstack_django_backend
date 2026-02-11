from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Chat
from .serializers import ChatSerializer, UserEmailActionSerializer
from users.models import CustomUser

class ChatRoomView(ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Показываем только те чаты, где юзер — владелец или участник
        user = self.request.user
        return Chat.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        # Скрытая операция: владелец берется из JWT токена
        serializer.save(owner=self.request.user)

class AddUserToChatView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEmailActionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat = get_object_or_404(Chat, id=serializer.validated_data['chat_id'], owner=request.user)
        user_to_add = CustomUser.objects.get(email=serializer.validated_data['email'])

        if user_to_add == request.user:
            return Response({"detail": "You are the owner."}, status=status.HTTP_400_BAD_REQUEST)
        
        if chat.members.filter(id=user_to_add.id).exists():
            return Response({"detail": "User already in chat."}, status=status.HTTP_400_BAD_REQUEST)

        chat.members.add(user_to_add)
        return Response({"message": "User added successfully."}, status=status.HTTP_200_OK)

class RemoveUserFromChatView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEmailActionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat = get_object_or_404(Chat, id=serializer.validated_data['chat_id'], owner=request.user)
        user_to_remove = CustomUser.objects.get(email=serializer.validated_data['email'])

        if not chat.members.filter(id=user_to_remove.id).exists():
            return Response({"detail": "User not in this chat."}, status=status.HTTP_400_BAD_REQUEST)

        chat.members.remove(user_to_remove)
        return Response({"message": "User removed successfully."}, status=status.HTTP_200_OK)