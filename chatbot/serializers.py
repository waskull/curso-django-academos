from rest_framework import serializers
from .models import OllamaConversation

class OllamaConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OllamaConversation
        fields = '__all__'
        read_only_fields = ('created_at',)

class ChatRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    model = serializers.CharField(default='deepseek-r1')
    context = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True
    )
    stream = serializers.BooleanField(default=False)
