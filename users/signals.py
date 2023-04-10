from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ChatBot, AudioFiles, VideoFiles
import uuid


@receiver(pre_save, sender=ChatBot)
def generate_chatbotID(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]

@receiver(pre_save, sender=AudioFiles)
def generate_audiofilesID(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]


@receiver(pre_save, sender=VideoFiles)
def generate_videofilesID(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:25]