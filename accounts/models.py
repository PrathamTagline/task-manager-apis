import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

def user_profile_upload_path(instance, filename):
    return f"user_media/{instance.id}/profile/{filename}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        if not password:
            raise ValueError('The Password field must be set')
        
        if not extra_fields.get('username'):
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    profile_iamge = models.ImageField(upload_to=user_profile_upload_path, null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Save the user instance first
        super().save(*args, **kwargs)

        # Ensure the profile image is saved to the correct path
        if self.profile_iamge and not self.profile_iamge.name.startswith(f"user_media/{self.id}/profile/"):
            self.profile_iamge.name = user_profile_upload_path(self, self.profile_iamge.name)
            super().save(*args, **kwargs)
