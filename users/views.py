from .forms import GenerateAudioFileForm, UploadAudioFileForm, UploadVideoFileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import AudioFiles, VideoFiles
from authentication.models import User
from gtts.tts import gTTSError
from openai.error import RateLimitError
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from openai import error
from gtts import gTTS
import openai as ai
import environ
import uuid
import os

env = environ.Env()
environ.Env.read_env()

def index_view(request):
    form = GenerateAudioFileForm()

    if request.method == 'POST':
        form = GenerateAudioFileForm(request.POST)

        if form.is_valid():
            new_audio_file = form.save(commit=False)
            print(f'Language accent: {new_audio_file.accent}')

            try:
                tts = gTTS(text=new_audio_file.description, lang='en', slow=False)   # default accent
                
                if new_audio_file.accent == "com.au":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)
                elif new_audio_file.accent == "com.uk":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)
                elif new_audio_file.accent == "us":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)
                elif new_audio_file.accent == "ca":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)
                elif new_audio_file.accent == "co.in":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)
                elif new_audio_file.accent == "ie":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)
                elif new_audio_file.accent == "co.za":
                    tts = gTTS(text=new_audio_file.description, lang='en', tld=str(new_audio_file.accent), slow=False)

                # Check if the user is authenticated
                if request.user.is_authenticated is False:
                    anonymous_user_username = "AnonymousUser" + str(uuid.uuid4()).replace('-', '')[:10]
                    anonymous_user_email = "anonymoususer" + str(uuid.uuid4()).replace('-', '')[:4] + "@unknown-email.x"
                    user = User.objects.create_user(username=anonymous_user_username, email=anonymous_user_email)
                    user.save()

                    new_audio_file.name = user
                
                    gen_audio = str('Anonymous/') + str(new_audio_file.title) + str(new_audio_file.file_type)
                    tts.save(str(settings.MEDIA_ROOT) + '/' + gen_audio)
                    new_audio_file.save()

                    # automatically download the audio file.
                    # a prompt may appear on some browsers -> depending on user's browser configuration.
                    audio_file = str(settings.MEDIA_ROOT) + '/' + gen_audio
                    response = HttpResponse(open(audio_file, 'rb').read())
                    response['Content-Type'] = 'audio/' + gen_audio[-3:]     # set Content-type to "audio/wav" or "audio/mp3" or "audio/ogg"
                    response['Content-Disposition'] = f'attachment; filename={gen_audio}'
                    os.remove(audio_file)   # delete uploaded audio file
                    return response
                
                messages.success(request, 'Audio file generated successfully')
                return redirect('index')

            except gTTSError:
                lang_acc = ''
                if new_audio_file.accent == 'com.au': lang_acc = 'Australia'
                elif new_audio_file.accent == 'ca': lang_acc = 'Canada'
                elif new_audio_file.accent == 'co.in': lang_acc = 'India'
                elif new_audio_file.accent == 'ie': lang_acc = 'Ireland'
                elif new_audio_file.accent == 'com.uk': lang_acc = 'UK'
                else:
                    lang_acc = 'US'

                messages.warning(request, f'Language accent "{lang_acc}" seems to unavailable. Please try again later!')

    context = {'GenerateAudioFileForm': form}
    return render(request, 'users/index.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def homepage_view(request):
    audio_form  = UploadAudioFileForm()
    video_form = UploadVideoFileForm()

    if request.method == 'POST':
        audio_form = UploadAudioFileForm(request.POST, request.FILES)
        video_form = UploadVideoFileForm(request.POST, request.FILES)
        
        # code to delete audio or video files
        delete_request = request.POST.get('delete-file')
        print(f'delete-request: {delete_request}')

        if AudioFiles.objects.filter(id=delete_request, name=request.user).exists():
            audio_files_qs = AudioFiles.objects.get(id=delete_request, name=request.user)
            audio_files_qs.delete()
            messages.error(request, f'You have deleted file: "{str(audio_files_qs.audio)[7:]}"')
        
        elif VideoFiles.objects.filter(id=delete_request, name=request.user).exists():
            video_files_qs = VideoFiles.objects.get(id=delete_request, name=request.user)
            video_files_qs.delete()
            messages.error(request, f'You have deleted file: "{video_files_qs.video[7:]}')
        

        if audio_form.is_valid():
            try:
                form = audio_form.save(commit=False)
                form.name = request.user
                form.save()

                # Use OpenAI module to translate audio file
                audio_file = form.audio # get the audio file
                user = AudioFiles.objects.get(name=request.user, audio=audio_file)   # get user instance with the uploaded audio file

                model_id = 'whisper-1'
                audio_file_path = str(settings.MEDIA_ROOT) + '/' + str(user.audio)      # audio file path
                saved_audio_file = open(audio_file_path, 'rb')    # open and read the audio file in binary format

                response = ai.Audio.transcribe(api_key=env('API_KEY'), model=model_id, file=saved_audio_file)   # transcribe the audio file using Open AI API
                
                # save transcribed audio in a text or .srt file
                file_name = str(request.user) + str(uuid.uuid4()).replace('-', '').upper()[:10] + '.txt'
                text_file_path = str(settings.MEDIA_ROOT) + '/User-files/' + str(file_name)
                
                with open(text_file_path, 'a') as file:
                    print(str(response.text), file=file)
                    file.close()

                response = HttpResponse(open(text_file_path, 'rb').read())
                response['Content-Type'] = 'audio' + file_name[-3:]
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                os.remove(text_file_path)       # delete text file

                return response

            except RateLimitError:
                messages.warning(request, 'Service is currently down! We are doing our best to make sure we are up and running!')
                return redirect('homepage')

        elif video_form.is_valid():
            form = video_form.save(commit=False)
            form.name = request.user
            form.save()

            messages.success(request, 'Form submitted successfully!')

            video_file = form.video
            user = VideoFiles.objects.get(name=request.user, video=video_file)   # get user instance with the uploaded video file
            
            model_id = 'whisper-1'
            media_file_path = str(settings.MEDIA_ROOT) + '/' + str(user.video)      # video file path
            saved_video_file = open(media_file_path, 'rb')    # open and read the video file in binary format
            
            try:
                response = ai.Audio.translate(api_key=env('API_KEY'), model=model_id, file=saved_video_file)   # transcribe the video file using Open AI API
                
                # save transcribed video in a text or .srt file
                file_name = str(request.user) + str(uuid.uuid4()).replace('-', '').upper()[:10] + form.file_type
                file_path = str(settings.MEDIA_ROOT) + '/User-files/' + str(file_name)
                
                with open(file_path, 'a') as file:
                    print(str(response.text), file=file)
                    file.close()

                response = HttpResponse(open(file_path, 'rb').read())
                response['Content-Type'] = 'text/plain'
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                os.remove(file_path)       # delete generated file

                return response
            
            except error.APIConnectionError:
                messages.warning(request, "Couldn't process your request! Check your internet connection.")
            
        return redirect('homepage')

    user_audio_files = AudioFiles.objects.filter(name=request.user).all()
    user_video_files = VideoFiles.objects.filter(name=request.user).all()

    context = {
        'UploadAudioForm': audio_form, 'UploadVideoForm': video_form, 'audio_files': user_audio_files,
        'video_files': user_video_files,
        }
    return render(request, 'users/homepage.html', context)

