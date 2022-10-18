from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(upload_to="profile_images", blank=True)
    github_url = models.URLField(blank=True)
