from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import ChatMessage
import json
import uuid
from groq import Groq
import logging

logger = logging.getLogger(__name__)

def get_or_create_session_id(request):
    """Get or create a session ID for the user"""
    if 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())
    return request.session['session_id']

def chat_view(request):
    """Main chat interface view"""
    session_id = get_or_create_session_id(request)
    
    # Get last 20 chat messages for this session
    chat_history = ChatMessage.objects.filter(
        session_id=session_id
    ).order_by('timestamp')[:20]
    
    return render(request, 'chat/index.html', {
        'chat_history': chat_history,
        'session_id': session_id
    })

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Handle AJAX requests to send messages to Groq API"""
    try:
        # Parse JSON data
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'error': 'Message cannot be empty'
            }, status=400)
        
        # Get session ID
        session_id = get_or_create_session_id(request)
        
        # Initialize Groq client
        if not settings.GROQ_API_KEY:
            return JsonResponse({
                'error': 'Groq API key not configured'
            }, status=500)
        
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Get recent chat history for context
        recent_messages = ChatMessage.objects.filter(
            session_id=session_id
        ).order_by('timestamp')[:5]
        
        # Build conversation context
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
            }
        ]
        
        # Add recent chat history for context
        for msg in recent_messages:
            messages.extend([
                {"role": "user", "content": msg.user_message},
                {"role": "assistant", "content": msg.ai_response}
            ])
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call Groq API
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192",  # Use Groq's Llama model
                temperature=0.7,
                max_tokens=1024,
                stream=False
            )
            
            ai_response = chat_completion.choices[0].message.content
            
        except Exception as api_error:
            logger.error(f"Groq API error: {str(api_error)}")
            return JsonResponse({
                'error': f'AI service error: {str(api_error)}'
            }, status=500)
        
        # Save to database
        try:
            chat_message = ChatMessage.objects.create(
                user_message=user_message,
                ai_response=ai_response,
                session_id=session_id
            )
            
            return JsonResponse({
                'success': True,
                'ai_response': ai_response,
                'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'message_id': chat_message.id
            })
            
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            return JsonResponse({
                'error': f'Database error: {str(db_error)}'
            }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'error': f'An unexpected error occurred: {str(e)}'
        }, status=500)

@require_http_methods(["POST"])
def clear_chat(request):
    """Clear chat history for current session"""
    try:
        session_id = get_or_create_session_id(request)
        ChatMessage.objects.filter(session_id=session_id).delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Chat history cleared'
        })
    
    except Exception as e:
        logger.error(f"Error clearing chat: {str(e)}")
        return JsonResponse({
            'error': f'Error clearing chat: {str(e)}'
        }, status=500)
