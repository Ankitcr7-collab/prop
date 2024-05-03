from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    company_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username + ' Profile'


class UserRoles(models.Model):
    is_moderator = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role")
    def __str__(self):
        if self.is_moderator == True:
            return f"moderator--{str(self.user)}"

# Signals
# Create profile instance 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance).save()