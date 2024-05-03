from django.contrib import admin

from django.contrib import admin
from .models import *

class PropertyImageAdmin(admin.StackedInline):
    model = PropertyImage

@admin.register(Properties)
class PropertyImgAdmin(admin.ModelAdmin):
    inlines = [PropertyImageAdmin]
    class Meta:
       model = Properties

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(FeatureMaster)
admin.site.register(TypeMaster)
admin.site.register(SavedSearch)

