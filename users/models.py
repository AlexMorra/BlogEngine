from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})

    def __str__(self):
        return self.email