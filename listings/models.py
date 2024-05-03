from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from geopy.geocoders import Nominatim
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta


class FeatureMaster(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return str(self.name)


class TypeMaster(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(TypeMaster, self).save(*args, **kwargs)


class Properties(models.Model):
    PROP_STATUS_CHOICES =(
    ("publish", "publish"),
    ("decline", "decline"),
    ("hold", "hold"),
    ("contract", "contract"),
    )

    is_ready_to_publish = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=PROP_STATUS_CHOICES, blank=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='properties')

    # Basic Information
    title = models.CharField(max_length=50)
    type = models.ManyToManyField(TypeMaster, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)

    # dimensions
    area_unit = models.CharField(max_length = 250, null = True, blank= True)
    buildup_area_unit = models.CharField(max_length = 250, null = True, blank= True)
    buildup_area = models.IntegerField(default=0, null=True, blank=True)
    carpet_area = models.IntegerField(default=0, null=True, blank=True)
    carpet_area_unit = models.CharField(max_length = 250, null = True, blank= True)
    bathroom = models.CharField(max_length = 10, null = True, blank= True)
    bedroom = models.CharField(max_length = 10, null = True, blank= True)

    # Location
    adddress = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    county = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=10)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)

    # Detailed Information
    content = models.TextField(default = "")
    feature = models.ManyToManyField(FeatureMaster, null=True, blank=True)

    # Media
    video_link = models.URLField(max_length=200)
    main_image = models.FileField(upload_to = 'properties', null=True, blank=True)
    pub_date = models.DateField(default=datetime.now())
    expire_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title 
    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        # self.city = self.city.lower()
        try:
            loc = self.adddress
            geolocator = Nominatim(user_agent="my_request")
            location = geolocator.geocode(loc)
            self.lat = location.latitude
            self.lon = location.longitude
        except:
            self.lat = self.lat
            self.lon = self.lon
        return super(Properties, self).save(*args, **kwargs)

@receiver(pre_save, sender=Properties)
def set_expire_date(sender, instance, *args, **kwargs):
    if not instance.expire_date:  # Set expire_date only if not already set
        instance.expire_date = instance.pub_date + timedelta(days=30)


class PropertyImage(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE, related_name="images")
    images = models.FileField(upload_to = 'properties', null=True, blank=True)
    def __str__(self):
        return self.property.title
    

class SavedSearch(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='searches')
    city = models.CharField(max_length=40)
    def __str__(self):
        return f"{str(self.user.username)} -- {self.city}"








