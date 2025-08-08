from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'session_id', 'user_message_preview', 'ai_response_preview']
    list_filter = ['timestamp', 'session_id']
    search_fields = ['user_message', 'ai_response']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def user_message_preview(self, obj):
        return obj.user_message[:50] + "..." if len(obj.user_message) > 50 else obj.user_message
    user_message_preview.short_description = "User Message"
    
    def ai_response_preview(self, obj):
        return obj.ai_response[:50] + "..." if len(obj.ai_response) > 50 else obj.ai_response
    ai_response_preview.short_description = "AI Response"