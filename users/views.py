from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import GenerateAudioFileForm, UploadAudioFileForm
from authentication.models import User
import speech_recognition as sr
from gtts import gTTS
import uuid
import os


def index_view(request):
    form = GenerateAudioFileForm()

    if request.method == 'POST':
        form = GenerateAudioFileForm(request.POST)

        if form.is_valid():
            new_audio_file = form.save(commit=False)

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
                return response

            else:
                new_audio_file.name = request.user
                gen_audio = str('Anonymous/') + str(new_audio_file.title) + str(new_audio_file.file_type)
                tts.save(str(settings.MEDIA_ROOT) + '/' + gen_audio)

                new_audio_file.save()


            messages.success(request, 'Audio file generated successfully')
            return redirect('index')

    context = {'GenerateAudioFileForm': form}
    return render(request, 'users/index.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def homepage_view(request):
    audio_form  = UploadAudioFileForm()    

    if request.method == 'POST':
        audio_form = UploadAudioFileForm(request.POST, request.FILES)
        if audio_form.is_valid():
            form = audio_form.save(commit=False)

            r = sr.Recognizer()
            file = sr.AudioFile(form.audio)
            with file as source:
                audio = r.record(source)
                r.recognize_google(audio)

                print(f'Audio: {r.recognize_google(audio)}')

            messages.success(request, 'Form submitted successfuly!')
            return redirect('homepage')


    context = {'UploadAudioForm': audio_form}
    return render(request, 'users/homepage.html', context)

