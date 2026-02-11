from django.urls import path
from .views import ChatRoomView, AddUserToChatView, RemoveUserFromChatView

app_name = 'chatroom'

urlpatterns = [
    path('', ChatRoomView.as_view(), name='chat-list'),
    path('add_user/', AddUserToChatView.as_view(), name='add-user'),
    path('remove_user/', RemoveUserFromChatView.as_view(), name='remove-user'),
]