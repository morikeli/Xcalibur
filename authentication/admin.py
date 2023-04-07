from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User
from .forms import SignupForm
from .models import User

class UserLayout(UserAdmin):
    model = User
    add_form = SignupForm
    list_display = ['username', 'email', 'gender', 'is_staff', 'date_joined',]

admin.site.register(User, UserLayout)
