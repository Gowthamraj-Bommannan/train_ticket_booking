from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
import pytz

ASIA_KOLKATA = pytz.timezone('Asia/Kolkata')

class Role(models.Model):
    """
    Model representing a user role in the system.

    Fields:
        - name (CharField): The name of the role. Choices are 'admin' and 'passenger'.
    """
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
    """
    Custom user model extending Django's AbstractUser.

    Fields:
        - username (CharField): Unique username for the user.
        - email (EmailField): Unique email address for the user.
        - mobile_number (CharField): Unique mobile number for the user.
        - first_name (CharField): User's first name.
        - last_name (CharField): User's last name (optional).
        - role (ForeignKey): Reference to the user's role (admin or passenger).
        - last_login (DateTimeField): Timestamp of the user's last login (auto-updated).

    Methods:
        - save(): Overrides the default save method to update last_login with Asia/Kolkata timezone.
        - __str__(): Returns the username as the string representation.
    """
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
        """
        Save the user instance, updating last_login to the current time in Asia/Kolkata timezone.
        """
        self.last_login = timezone.now().astimezone(ASIA_KOLKATA)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
