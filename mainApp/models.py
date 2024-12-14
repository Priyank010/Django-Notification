from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Allows flexibility to add more fields in the future.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Change the related_name to avoid conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Change the related_name to avoid conflicts
        blank=True
    )

    def __str__(self):
        return self.username

class Notification(models.Model):
    """
    Notification model linked to the CustomUser model.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically use the custom user model
        on_delete=models.CASCADE,
        related_name="notifications"  # Each user will have a related set of notifications
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title