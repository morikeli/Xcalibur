from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm, EditProfileForm


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'


def signup_view(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')

    context = {'SignupForm': form}
    return render(request, 'authentication/signup.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def user_profile_view(request):
    form = EditProfileForm(instance=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.warning(request, 'You have updated your profile!')
            return redirect('user_profile')

    context = {'EditProfileForm': form}
    return render(request, 'authentication/profile.html', context)


class LogoutUser(LogoutView):
    template_name = 'authentication/logout.html'
