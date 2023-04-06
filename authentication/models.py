from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    email = models.EmailField(unique=True, blank=False)
    gender = models.CharField(max_length=7, blank=False)
    phone_no = models.CharField(max_length=14, blank=False)
    profile_pic = models.ImageField(upload_to='Users-Dps/', default='default.png')
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        ordering = ['username']
         