from django.db import models 
from django.contrib.auth.models import User

class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models. CASCADE) 
    image = models. ImageField(upload_to='avatars/', null=True, blank=True) 
    nickname = models.CharField(max_length=30, null=True, blank=True) 
    email = models.EmailField(unique=True, null=True) 
    location = models.CharField(max_length=30, null=True, blank=True) 
    bio = models. TextField(null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
