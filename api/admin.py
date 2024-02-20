from django.contrib import admin
from .models import Dweet, Profile, Follow


# Register your models here.
admin.site.register(Dweet)
admin.site.register(Profile)
admin.site.register(Follow)
