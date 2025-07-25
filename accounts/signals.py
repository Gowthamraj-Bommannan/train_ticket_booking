from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Role

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    """
    Signal handler to create default roles ('admin' and 'passenger') after migrations.
    This ensures that the Role table always contains the required roles.
    Triggered after migrations for the accounts app.
    """
    if sender.name == 'accounts':
        Role.objects.get_or_create(name=Role.ADMIN)
        Role.objects.get_or_create(name=Role.PASSENGER)

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    """
    Signal handler to create a default admin user after migrations.
    If no user with the admin role exists, creates a superuser with default credentials.
    Triggered after migrations for the accounts app.
    """
    if sender.name == 'accounts':
        User = get_user_model()
        admin_role, _ = Role.objects.get_or_create(name=Role.ADMIN)
        if not User.objects.filter(role=admin_role).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@trainbooking.com',
                password='admin123',
                mobile_number='9999999999',
                first_name='Admin',
                role=admin_role
            ) 