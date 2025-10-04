from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class OllamaConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    response = models.TextField()
    model_used = models.CharField(max_length=100)
    context = models.JSONField(null=True, blank=True)  # Para almacenar el array de contexto
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Métricas de rendimiento
    total_duration = models.BigIntegerField(null=True, blank=True)  # en nanosegundos
    prompt_eval_count = models.IntegerField(null=True, blank=True)
    eval_count = models.IntegerField(null=True, blank=True)
    prompt_eval_duration = models.BigIntegerField(null=True, blank=True)
    eval_duration = models.BigIntegerField(null=True, blank=True)
    load_duration = models.BigIntegerField(null=True, blank=True)
    
    # Información de finalización
    done = models.BooleanField(default=True)
    done_reason = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.prompt[:50]}... - {self.created_at}"