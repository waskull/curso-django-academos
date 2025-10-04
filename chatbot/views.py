import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import OllamaConversation
from .serializers import ChatRequestSerializer, OllamaConversationSerializer

class ChatbotView(APIView):
    """
    Vista para manejar las peticiones del chatbot con Ollama
    """
    
    def post(self, request):
        # Validar los datos de entrada
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extraer datos validados
        prompt = serializer.validated_data['prompt']
        model = serializer.validated_data['model']
        context = serializer.validated_data.get('context')
        stream = serializer.validated_data.get('stream', False)
        
        # Preparar payload para Ollama
        ollama_payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        # Agregar contexto si está disponible
        if context:
            ollama_payload["context"] = context
        
        try:
            # Hacer petición a Ollama
            response = requests.post(
                'http://localhost:11434/api/generate',
                json=ollama_payload,
                timeout=60  # 60 segundos de timeout
            )
            response.raise_for_status()
            ollama_data = response.json()
            
        except requests.exceptions.ConnectionError:
            return Response(
                {'error': 'No se puede conectar con Ollama. Asegúrate de que esté ejecutándose en localhost:11434'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except requests.exceptions.Timeout:
            return Response(
                {'error': 'Timeout al conectar con Ollama'},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Error en la comunicación con Ollama: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Guardar la conversación en la base de datos
        conversation = OllamaConversation(
            user=request.user if request.user.is_authenticated else None,
            prompt=prompt,
            response=ollama_data.get('response', ''),
            model_used=model,
            context=ollama_data.get('context'),
            total_duration=ollama_data.get('total_duration'),
            prompt_eval_count=ollama_data.get('prompt_eval_count'),
            eval_count=ollama_data.get('eval_count'),
            prompt_eval_duration=ollama_data.get('prompt_eval_duration'),
            eval_duration=ollama_data.get('eval_duration'),
            load_duration=ollama_data.get('load_duration'),
            done=ollama_data.get('done', True),
            done_reason=ollama_data.get('done_reason')
        )
        conversation.save()
        
        # Preparar respuesta para el cliente
        response_data = {
            'response': ollama_data.get('response', ''),
            'context': ollama_data.get('context'),
            'conversation_id': conversation.id,
            'metrics': {
                'total_duration_seconds': ollama_data.get('total_duration', 0) / 1_000_000_000,
                'prompt_eval_count': ollama_data.get('prompt_eval_count'),
                'eval_count': ollama_data.get('eval_count'),
                'done_reason': ollama_data.get('done_reason')
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class ConversationHistoryView(APIView):
    """
    Vista para obtener el historial de conversaciones
    """
    
    def get(self, request):
        if request.user.is_authenticated:
            conversations = OllamaConversation.objects.filter(user=request.user)
        else:
            # Si no hay usuario, puedes manejarlo de otra forma o devolver error
            conversations = OllamaConversation.objects.all()[:50]  # Últimas 50 conversaciones
        
        serializer = OllamaConversationSerializer(conversations, many=True)
        return Response(serializer.data)

class ConversationDetailView(APIView):
    """
    Vista para obtener los detalles de una conversación específica
    """
    
    def get(self, request, conversation_id):
        try:
            if request.user.is_authenticated:
                conversation = OllamaConversation.objects.get(id=conversation_id, user=request.user)
            else:
                conversation = OllamaConversation.objects.get(id=conversation_id)
            
            serializer = OllamaConversationSerializer(conversation)
            return Response(serializer.data)
            
        except OllamaConversation.DoesNotExist:
            return Response(
                {'error': 'Conversación no encontrada'},
                status=status.HTTP_404_NOT_FOUND)