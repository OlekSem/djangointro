from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
# Таблиці в БД
class CustomUser(AbstractUser):
    # image_small = ResizedImageField(
    #     size=[300, 300],
    #     crop=['middle', 'center'],
    #     quality=85,
    #     force_format='WEBP',
    #     upload_to=upload_avatar('small'),
    #     null=True,
    #     blank=True
    # )
    # image_medium = ResizedImageField(
    #     size=[800, 800],
    #     quality=85,
    #     force_format='WEBP',
    #     upload_to=upload_avatar('medium'),
    #     null=True,
    #     blank=True
    # )

    # image_large = ResizedImageField(
    #     size=[1200, 1200],
    #     quality=90,
    #     force_format='WEBP',
    #     upload_to=upload_avatar('large'),
    #     null=True,
    #     blank=True
    # )
    image_small = models.CharField(max_length=255, null=True, blank=True)
    image_medium = models.CharField(max_length=255, null=True, blank=True)
    image_large = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.email
    