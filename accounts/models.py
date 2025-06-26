from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
import pytz

ASIA_KOLKATA = pytz.timezone('Asia/Kolkata')

class Role(models.Model):
    ADMIN = 'admin'
    PASSENGER = 'passenger'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PASSENGER, 'Passenger'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'mobile_number', 'first_name']
    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        self.last_login = timezone.now().astimezone(ASIA_KOLKATA)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
