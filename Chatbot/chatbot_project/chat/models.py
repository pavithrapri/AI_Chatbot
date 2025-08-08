from django.db import models
from django.utils import timezone

class ChatMessage(models.Model):
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    session_id = models.CharField(max_length=255, default='default')

    class Meta:
        ordering = ['-timestamp']
        db_table = 'chat_messages'

    def __str__(self):
        return f"Chat at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
