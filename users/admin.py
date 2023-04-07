from django.contrib import admin
from .models import ChatBot, Audios


@admin.register(ChatBot)
class ChatBotInfoTable(admin.ModelAdmin):
    list_display = ['name', 'speaker', 'created']
    readonly_fields = ['speaker']


@admin.register(Audios)
class AudioFilesRecordsTable(admin.ModelAdmin):
    list_display = ['name', 'title', 'file_type', 'created']
    readonly_fields = ['title', 'description', 'file_type', 'created']
