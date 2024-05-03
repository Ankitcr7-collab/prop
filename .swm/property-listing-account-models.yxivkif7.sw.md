---
title: Property Listing Account models
---
<SwmSnippet path="/accounts/models.py" line="1">

---

**User profile and User Roles** 

This code defines two Django models, `UserProfile` and `UserRoles`, which are related to the built-in `User` model. `UserProfile` has fields for a profile picture, company logo, company name, and mobile number. `UserRoles` has a boolean field for indicating if the user is a moderator. The code also includes a signal `post_save` to create a `UserProfile` instance whenever a `User` instance is created.

```python
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
```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBcHJvcCUzQSUzQUFua2l0Y3I3LWNvbGxhYg==" repo-name="prop"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
