from django.contrib import admin
from .models import ChatBot, AudioFiles, VideoFiles


@admin.register(ChatBot)
class ChatBotInfoTable(admin.ModelAdmin):
    list_display = ['name', 'speaker', 'created']
    readonly_fields = ['speaker']


@admin.register(AudioFiles)
class AudioFilesRecordsTable(admin.ModelAdmin):
    list_display = ['name', 'title', 'file_type', 'created']
    readonly_fields = ['title', 'description', 'audio', 'file_type', 'created']


@admin.register(VideoFiles)
class VideoFilesRecordsTable(admin.ModelAdmin):
    list_display = ['name', 'title', 'file_type', 'created']
    readonly_fields = ['title', 'video', 'file_type', 'created']
