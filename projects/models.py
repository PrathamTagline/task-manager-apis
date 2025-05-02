import uuid
from django.db import models
from accounts.models import User


def project_image_path(instance, filename):
    return f"project_media/{instance.id}/images/{filename}"

class Project(models.Model):
    """
    Represents a project with metadata, image, assigned users, and a unique key.
    """
    PROJECT_TYPE_CHOICES = [
        ('WEB', 'Web'),
        ('API', 'API'),
        ('MOBILE', 'Mobile'),
        ('DESKTOP', 'Desktop'),
        ('OTHER', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    key = models.CharField(max_length=10, unique=True, blank=True)
    type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES, default='OTHER')
    image = models.ImageField(upload_to=project_image_path, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.key})"
    
    def generate_unique_key(self):
        """
        Generate a unique key based on the project name.
        One word: use uppercase word.
        Multiple words: use initials in uppercase.
        Append letter suffix (A, B, ... AA, AB, etc.) until key is unique.
        """
        words = [word for word in self.name.split() if word.isalpha()]
        base_key = words[0].upper() if len(words) == 1 else ''.join(word[0].upper() for word in words)
        key = base_key
        suffix_index = 0

        while Project.objects.filter(key=key).exclude(pk=self.pk).exists():
            key = f"{base_key}{self.index_to_letters(suffix_index)}"
            suffix_index += 1

        return key

    @staticmethod
    def index_to_letters(index):
        """
        Convert an integer to an alphabetical string (e.g., 0 -> A, 26 -> AA).
        """
        result = ""
        while True:
            index, rem = divmod(index, 26)
            result = chr(65 + rem) + result
            if index == 0:
                break
            index -= 1
        return result

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # Check if the name has changed and regenerate the key
        if not is_new and Project.objects.filter(pk=self.pk).exists():
            original = Project.objects.get(pk=self.pk)
            if original.name != self.name:
                self.key = self.generate_unique_key()

        # Generate a key for new projects if not already set
        if not self.key:
            self.key = self.generate_unique_key()

        # Save the instance first to ensure the ID is generated
        super().save(*args, **kwargs)

        if is_new and self.image:
            # Store the uploaded image in the correct path
            uploaded_image = self.image
            self.image = None  # Temporarily clear the image field
            image_path = project_image_path(self, uploaded_image.name)
            self.image.save(image_path, uploaded_image.file, save=False)
            super().save(update_fields=['image'])

class ProjectMembership(models.Model):
    """
    Model representing a user's membership in a project with a specific role.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('DEVELOPER', 'Developer'),
        ('TESTER', 'Tester'),
        ('DESIGNER', 'Designer'),
        ('OTHER', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OTHER')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project') 

    def __str__(self):
        return f"{self.user.email} - {self.project.name} ({self.role})"