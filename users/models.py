from authentication.models import User
from django.db import models


class ChatBot(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    name = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    speaker = models.CharField(max_length=7, blank=False, db_column='voice')   # male voice or female voice
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name', 'speaker']
        verbose_name_plural = 'Chat Bot Records'
        

class Audios(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    name = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=False)
    audio = models.FileField(upload_to='Audios/', null=False, editable=False)
    accent = models.CharField(max_length=20, blank=True)
    file_type = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name', 'audio']
        verbose_name_plural = 'Audio Files Records'

