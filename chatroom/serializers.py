from rest_framework import serializers
from .models import Chat
from users.models import CustomUser

class ChatSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "name", "owner", "owner_email", "members", "created_at"]
        read_only_fields = ["owner", "created_at", "members"]


class UserEmailActionSerializer(serializers.Serializer):
    """Валидатор для действий с пользователями через Email"""
    chat_id = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email not found.")
        return value

    def validate_chat_id(self, value):
        if not Chat.objects.filter(id=value).exists():
            raise serializers.ValidationError("Chat not found.")
        return value