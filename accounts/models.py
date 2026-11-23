from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra data for each user. Created automatically by a signal."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def str(self):
        return f'Profile of {self.user.username}'
