from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class SignupForm(UserCreationForm):
    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'mb-2', 'autofocus': True}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'mb-2'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'mb-2'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'type': 'email', 'class': 'mb-2'}), required=True)
    gender = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select', 'class': 'mb-2'}), choices=SELECT_GENDER)
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'mb-2'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'gender', 'email', 'phone_no', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone_no', 'profile_pic']

