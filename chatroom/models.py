from django.conf import settings
from django.db import models

class Chat(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="owned_chats"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chats",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name