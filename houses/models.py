from django.db import models
from django.contrib.auth.models import User


class House(models.Model):
    """
    House model, related to 'owner(user instance)'.
    Default image set so that we can reference image.url
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, max_length=600)
    image = models.ImageField(
        upload_to='images/', default='../default-house_od6n9o',
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
